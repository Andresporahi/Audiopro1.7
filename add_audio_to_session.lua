-- ReaScript para agregar audio a sesión de Reaper
-- AudioPro v1.7 - Reaper Edition
-- Según documentación: https://www.reaper.fm/sdk/reascript/reascripthelp.html#lua_list

-- Obtener parámetros usando ExtState (según documentación de ReaScript)
local audio_file = reaper.GetExtState("AudioPro", "audio_file")
local session_name = reaper.GetExtState("AudioPro", "session_name")
local template_path = reaper.GetExtState("AudioPro", "template_path")
local original_name = reaper.GetExtState("AudioPro", "original_name")

-- Debug: log de parámetros recibidos
reaper.ShowConsoleMsg("=== AudioPro v1.7 - Reaper Script ===\n")
reaper.ShowConsoleMsg("Audio file: " .. audio_file .. "\n")
reaper.ShowConsoleMsg("Session name: " .. session_name .. "\n")
reaper.ShowConsoleMsg("Template path: " .. template_path .. "\n")
reaper.ShowConsoleMsg("Original name: " .. original_name .. "\n")

-- DEBUG: Logs en consola (sin cuadros de diálogo)
-- Para ver logs: Extensions > ReaScript > Show console output

if audio_file == "" or session_name == "" or template_path == "" then
    reaper.MB("Error: Faltan parámetros (archivo de audio, sesión y template)", "AudioPro Error", 0)
    return
end

-- Verificar que el archivo de audio existe
if not reaper.file_exists(audio_file) then
    reaper.MB("Error: El archivo de audio no existe: " .. audio_file, "AudioPro Error", 0)
    return
end

-- Verificar que el archivo no esté vacío y validar formato WAV
local file = io.open(audio_file, "rb")
if file then
    local size = file:seek("end")
    file:seek("set", 0)
    
    -- Leer header WAV (primeros 12 bytes)
    local riff = file:read(4)
    local file_size = file:read(4)
    local wave = file:read(4)
    
    file:close()
    
    reaper.ShowConsoleMsg("Tamaño del archivo de audio: " .. size .. " bytes\n")
    reaper.ShowConsoleMsg("Header RIFF: " .. (riff or "null") .. "\n")
    reaper.ShowConsoleMsg("Header WAVE: " .. (wave or "null") .. "\n")
    
    if size < 1000 then
        reaper.MB("Error: El archivo de audio está vacío o es demasiado pequeño: " .. size .. " bytes", "AudioPro Error", 0)
        return
    end
    
    if riff ~= "RIFF" or wave ~= "WAVE" then
        reaper.MB("Error: El archivo no es un WAV válido. Header: " .. (riff or "null") .. " " .. (wave or "null"), "AudioPro Error", 0)
        return
    end
else
    reaper.MB("Error: No se pudo abrir el archivo de audio", "AudioPro Error", 0)
    return
end

-- Convertir ruta a formato Windows (backslashes)
local audio_file_windows = audio_file:gsub("/", "\\")
reaper.ShowConsoleMsg("Ruta original: " .. audio_file_windows .. "\n")

-- Verificar si el archivo ya está en F:\00\00 Reaper\Eleven\
local eleven_dir = "F:\\00\\00 Reaper\\Eleven"
local is_in_eleven = string.find(audio_file_windows, eleven_dir, 1, true) ~= nil

if is_in_eleven then
    reaper.ShowConsoleMsg("El archivo ya está en Eleven, usando directamente\n")
    audio_file = audio_file_windows
else
    -- Copiar archivo a ubicación permanente en F:\00\00 Reaper\Eleven\
    local timestamp = os.date("%Y%m%d_%H%M%S")
    local audio_copy = eleven_dir .. "\\audio_" .. timestamp .. ".wav"
    
    reaper.ShowConsoleMsg("Copiando audio temporal a Eleven: " .. audio_copy .. "\n")
    
    -- Copiar archivo usando Lua
    local source = io.open(audio_file_windows, "rb")
    local dest = io.open(audio_copy, "wb")
    if source and dest then
        local content = source:read("*all")
        dest:write(content)
        source:close()
        dest:close()
        reaper.ShowConsoleMsg("Archivo copiado exitosamente a Eleven\n")
        -- Usar la copia para insertar
        audio_file = audio_copy
    else
        reaper.MB("Error: No se pudo copiar el archivo de audio a " .. audio_copy, "AudioPro Error", 0)
        return
    end
end

-- Verificar que el template existe
if not reaper.file_exists(template_path) then
    reaper.MB("Error: Template no encontrado: " .. template_path, "AudioPro Error", 0)
    return
end

-- Cargar template y crear nueva sesión
reaper.Main_openProject(template_path)

-- Esperar un momento para que el proyecto se cargue completamente
reaper.defer(function() end)

-- Hacer "Save As" con el nuevo nombre usando Main_SaveProjectEx
-- Según documentación: Main_SaveProjectEx(proj, filename, flags)
-- flags = 0 para "Save As"
reaper.ShowConsoleMsg("Guardando sesión como: " .. session_name .. "\n")
reaper.Main_SaveProjectEx(0, session_name, 0)

-- Verificar que el archivo se creó
if reaper.file_exists(session_name) then
    reaper.ShowConsoleMsg("Sesión guardada exitosamente\n")
else
    reaper.MB("Error: No se pudo verificar que la sesión se guardó: " .. session_name, "AudioPro Error", 0)
    return
end

-- Buscar la pista llamada "Clase" (con mayúscula)
local track = nil
local track_count = reaper.CountTracks(0)

reaper.ShowConsoleMsg("Buscando pista 'Clase'...\n")
reaper.ShowConsoleMsg("Total de pistas: " .. track_count .. "\n")

-- DEBUG: Listar todas las pistas
local tracks_list = "Pistas encontradas (" .. track_count .. "):\n\n"

for i = 0, track_count - 1 do
    local current_track = reaper.GetTrack(0, i)
    local _, track_name = reaper.GetSetMediaTrackInfo_String(current_track, "P_NAME", "", false)
    
    tracks_list = tracks_list .. i .. ": '" .. track_name .. "'\n"
    reaper.ShowConsoleMsg("Pista " .. i .. ": '" .. track_name .. "'\n")
    
    -- Buscar "Clase" (case-insensitive para mayor compatibilidad)
    if track_name:lower() == "clase" then
        track = current_track
        reaper.ShowConsoleMsg("¡Pista 'Clase' encontrada en índice " .. i .. "!\n")
        break
    end
end

-- DEBUG: Mostrar lista de pistas
reaper.MB(tracks_list, "AudioPro Debug - Pistas", 0)

if not track then
    reaper.MB("Error: No se encontró la pista 'Clase'", "AudioPro Error", 0)
    reaper.ShowConsoleMsg("ERROR: No se encontró la pista 'Clase'\n")
    return
end

-- Seleccionar solo la pista "Clase"
reaper.SetOnlyTrackSelected(track)

-- Establecer la pista como activa para la inserción
reaper.SetTrackSelected(track, true)

-- Insertar el archivo de audio MANUALMENTE usando AddMediaItemToTrack
reaper.SetEditCurPos(0, false, false) -- Mover cursor al inicio

reaper.ShowConsoleMsg("Insertando audio en pista 'Clase' manualmente...\n")
reaper.ShowConsoleMsg("Archivo de audio: " .. audio_file .. "\n")

-- Crear nuevo ítem en la pista
local item = reaper.AddMediaItemToTrack(track)

if item then
    -- Agregar el archivo de audio como source del ítem
    local pcm_source = reaper.PCM_Source_CreateFromFile(audio_file)
    
    if pcm_source then
        -- Obtener duración del source
        local source_length = reaper.GetMediaSourceLength(pcm_source)
        reaper.ShowConsoleMsg("Duración del source PCM: " .. source_length .. " segundos\n")
        
        if source_length > 0 then
            -- Crear take y asignar source
            local take = reaper.AddTakeToMediaItem(item)
            reaper.SetMediaItemTake_Source(take, pcm_source)
            
            -- Configurar posición y duración del ítem
            reaper.SetMediaItemInfo_Value(item, "D_POSITION", 0) -- Posición 0
            reaper.SetMediaItemInfo_Value(item, "D_LENGTH", source_length) -- Duración del audio
            
            -- Actualizar ítem
            reaper.UpdateItemInProject(item)
            
            reaper.ShowConsoleMsg("¡Audio insertado exitosamente con duración: " .. source_length .. " segundos!\n")
            
            local item_length = source_length
            
            -- Configurar render según la imagen
            -- Extraer directorio y usar nombre original del archivo
            local session_dir = string.match(session_name, "(.+)[/\\]") or ""
            local output_file = session_dir .. "/" .. original_name .. "_renderizado.wav"
            
            -- Log de debug
            reaper.ShowConsoleMsg("Session dir: " .. session_dir .. "\n")
            reaper.ShowConsoleMsg("Original name: " .. original_name .. "\n")
            reaper.ShowConsoleMsg("Output file: " .. output_file .. "\n")
            
            -- Deseleccionar todos los ítems primero
            reaper.Main_OnCommand(40289, 0) -- Item: Unselect all items
            
            -- Seleccionar solo este ítem
            reaper.SetMediaItemSelected(item, true)
            
            -- Configurar time selection basada en el ítem
            local item_pos = reaper.GetMediaItemInfo_Value(item, "D_POSITION")
            local item_end = item_pos + item_length
        
        -- Establecer loop/time selection
        reaper.GetSet_LoopTimeRange(true, false, item_pos, item_end, false)
        
        reaper.ShowConsoleMsg("Time selection: " .. item_pos .. " - " .. item_end .. "\n")
        
        -- Configurar opciones de render según la imagen y documentación
        reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_file, true)
        
        -- Configuración de audio según imagen: 48kHz, Mono, 24-bit PCM
        reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true) -- 48kHz
        reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true) -- Mono (según imagen)
        
        -- WAV 24-bit PCM - formato base64 según documentación
        -- evaw = WAV format, luego configuración específica
        local wav_cfg = "ZXZhdxgAAAA=" -- Base64 para WAV 24-bit PCM
        reaper.GetSetProjectInfo_String(0, "RENDER_FORMAT", wav_cfg, true)
        
        -- Source: Master mix (0) en lugar de selected items
        reaper.GetSetProjectInfo(0, "RENDER_SETTINGS", 0, true)
        
        -- Bounds: Time selection (1)
        reaper.GetSetProjectInfo(0, "RENDER_BOUNDSFLAG", 1, true)
        
        -- Tail: 1000ms (1 segundo según imagen)
        reaper.GetSetProjectInfo(0, "RENDER_TAILFLAG", 1, true)
        reaper.GetSetProjectInfo(0, "RENDER_TAILMS", 1000, true)
        
        -- Resample mode (mejor calidad)
        reaper.GetSetProjectInfo(0, "RENDER_RESAMPLE", 2, true) -- 2 = Sinc interpolation
        
        -- Guardar sesión antes de renderizar
        reaper.Main_SaveProjectEx(0, session_name, 0)
        
        -- Renderizar usando el comando correcto
        reaper.Main_OnCommand(41824, 0) -- File: Render project, using the most recent render settings
        
        reaper.ShowConsoleMsg("=== Proceso completado exitosamente ===\n")
        reaper.ShowConsoleMsg("Reaper permanecerá abierto para revisar el resultado\n")
        
        -- NO cerrar Reaper automáticamente - dejar abierto para revisión
        -- El archivo renderizado se creará en: output_file
        else
            reaper.MB("Error: El source PCM tiene duración 0", "AudioPro Error", 0)
            reaper.ShowConsoleMsg("ERROR: source_length = 0\n")
        end
    else
        reaper.MB("Error: No se pudo crear PCM_Source desde el archivo", "AudioPro Error", 0)
        reaper.ShowConsoleMsg("ERROR: PCM_Source_CreateFromFile falló\n")
    end
else
    reaper.MB("Error: No se pudo crear ítem en la pista", "AudioPro Error", 0)
    reaper.ShowConsoleMsg("ERROR: AddMediaItemToTrack falló\n")
end
