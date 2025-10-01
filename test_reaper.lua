-- Script de prueba para Reaper
-- AudioPro v1.7 - Reaper Edition

-- Obtener argumentos
local args = {...}
local audio_file = args[1]
local session_name = args[2]

-- Mostrar argumentos recibidos
reaper.ShowMessageBox("Argumentos recibidos:\nAudio: " .. tostring(audio_file) .. "\nSesión: " .. tostring(session_name), "Test Reaper", 0)

-- Verificar que el template existe
local template_path = "F:\\00\\00 Reaper\\00 Voces.rpp"
if reaper.file_exists(template_path) then
    reaper.ShowMessageBox("✅ Template encontrado: " .. template_path, "Test Reaper", 0)
    
    -- Intentar cargar el template
    local success = reaper.Main_openProject(template_path)
    if success then
        reaper.ShowMessageBox("✅ Template cargado exitosamente", "Test Reaper", 0)
        
        -- Intentar guardar como nueva sesión
        if session_name then
            reaper.Main_SaveProject(0, session_name)
            reaper.ShowMessageBox("✅ Sesión guardada como: " .. session_name, "Test Reaper", 0)
        end
    else
        reaper.ShowMessageBox("❌ Error cargando template", "Test Reaper", 0)
    end
else
    reaper.ShowMessageBox("❌ Template no encontrado: " .. template_path, "Test Reaper", 0)
end
