param([string]$Video = (Join-Path $PSScriptRoot 'cam-video.mp4'))

# Plays a video file through OBS Virtual Camera so any app (Zoom, browser, TikTok Live Studio) sees it as a webcam.
$ErrorActionPreference = 'Stop'
$Video = (Resolve-Path $Video).Path
$obsDir = 'C:\Program Files\obs-studio\bin\64bit'
$cfg = Join-Path $env:APPDATA 'obs-studio'
$scenes = Join-Path $cfg 'basic\scenes'
$profile = Join-Path $cfg 'basic\profiles\VirtualCam'
New-Item -ItemType Directory -Force $scenes, $profile | Out-Null

# Skip the first-run wizard and select our profile and scene collection.
$ini = @"
[General]
FirstRun=true
EnableAutoUpdates=false
[Basic]
Profile=VirtualCam
ProfileDir=VirtualCam
SceneCollection=VirtualCam
SceneCollectionFile=VirtualCam
"@
foreach ($f in 'global.ini', 'user.ini') {
    $p = Join-Path $cfg $f
    if (-not (Test-Path $p)) { Set-Content -Path $p -Value $ini -Encoding UTF8 }
}

Set-Content -Path (Join-Path $profile 'basic.ini') -Encoding UTF8 -Value @"
[General]
Name=VirtualCam
[Video]
BaseCX=1280
BaseCY=720
OutputCX=1280
OutputCY=720
FPSType=0
FPSCommon=30
"@

$sceneId = '7c1d0b3e-5a51-4b7f-9b0a-1f3e2c4d5a61'
$videoId = '2f6e9a4b-8c3d-4e1f-a7b2-6d5c4b3a2918'
$collection = [ordered]@{
    name                  = 'VirtualCam'
    current_scene         = 'VirtualCam'
    current_program_scene = 'VirtualCam'
    scene_order           = @(@{ name = 'VirtualCam' })
    sources               = @(
        [ordered]@{
            id = 'scene'; versioned_id = 'scene'; name = 'VirtualCam'; uuid = $sceneId
            settings = [ordered]@{
                id_counter = 1
                items      = @([ordered]@{
                        name = 'Video'; source_uuid = $videoId; id = 1; visible = $true
                        pos = @{ x = 640.0; y = 360.0 }; align = 0; scale = @{ x = 1.0; y = 1.0 }
                        bounds_type = 2; bounds_align = 0; bounds = @{ x = 1280.0; y = 720.0 }
                    })
            }
        },
        [ordered]@{
            id = 'ffmpeg_source'; versioned_id = 'ffmpeg_source'; name = 'Video'; uuid = $videoId
            settings = [ordered]@{
                is_local_file = $true; local_file = $Video
                looping = $true; restart_on_activate = $true; hw_decode = $true
            }
        }
    )
}
$collection | ConvertTo-Json -Depth 10 | Set-Content -Path (Join-Path $scenes 'VirtualCam.json') -Encoding UTF8

Get-Process obs64 -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1
Start-Process -FilePath (Join-Path $obsDir 'obs64.exe') -WorkingDirectory $obsDir `
    -ArgumentList '--profile', 'VirtualCam', '--collection', 'VirtualCam', '--scene', 'VirtualCam', '--startvirtualcam', '--disable-shutdown-check'
Write-Host "Virtual camera started with: $Video"
