-- ReaScript para renderizar sesión de Reaper
-- AudioPro v1.7 - Reaper Edition

-- Obtener argumentos de línea de comandos
local args = {...}
local session_path = args[1]
local output_file = args[2]

if not session_path or not output_file then
    reaper.ShowMessageBox("Error: Faltan argumentos (sesión y archivo de salida)", "AudioPro Error", 0)
    return
end

-- Cargar la sesión
local retval = reaper.Main_openProject(session_path)
if not retval then
    reaper.ShowMessageBox("Error: No se pudo cargar la sesión: " .. session_path, "AudioPro Error", 0)
    return
end

-- Configurar render
reaper.GetSetProjectInfo(0, "RENDER_FILE", output_file, true)
reaper.GetSetProjectInfo(0, "RENDER_FORMAT", 3, true) -- WAV
reaper.GetSetProjectInfo(0, "RENDER_SRATE", 48000, true) -- 48kHz
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 2, true) -- Estéreo
reaper.GetSetProjectInfo(0, "RENDER_BITDEPTH", 16, true) -- 16-bit
reaper.GetSetProjectInfo(0, "RENDER_DITHER", 0, true) -- Sin dither
reaper.GetSetProjectInfo(0, "RENDER_NORMALIZE", 0, true) -- Sin normalizar
reaper.GetSetProjectInfo(0, "RENDER_TAILFLAG", 0, true) -- Sin tail
reaper.GetSetProjectInfo(0, "RENDER_TAILMS", 0, true) -- Sin tail ms

-- Renderizar
reaper.Main_OnCommand(41824, 0) -- Render project

-- Esperar un momento para que termine el render
reaper.defer(function()
    reaper.ShowMessageBox("✅ Render completado: " .. output_file, "AudioPro Success", 0)
end)
