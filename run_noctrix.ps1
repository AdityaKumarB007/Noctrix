# NOCTRIX Interactive PowerShell Control Menu
function Show-Menu {
    Clear-Host
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "                 NOCTRIX CONTROL CENTER & LAUNCHER                    " -ForegroundColor Yellow
    Write-Host "     Non-Human Identity Discovery, Graph Mapping & Remediation        " -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] Run Full Pipeline (Discovery -> Graph -> Risk -> Remediation)" -ForegroundColor White
    Write-Host "  [2] Launch Streamlit Visual Dashboard (Web UI)" -ForegroundColor White
    Write-Host "  [3] Run Automated Test Suite (pytest)" -ForegroundColor White
    Write-Host "  [4] Start Docker Containers (Neo4j & Vault)" -ForegroundColor White
    Write-Host "  [5] Stop Docker Containers" -ForegroundColor White
    Write-Host "  [6] Exit" -ForegroundColor Red
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
}

do {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-6)"
    switch ($choice) {
        "1" {
            Clear-Host
            Write-Host "[*] Executing NOCTRIX Pipeline Orchestrator..." -ForegroundColor Cyan
            python main.py
            Write-Host "`nPress any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "2" {
            Clear-Host
            Write-Host "[*] Starting Streamlit Dashboard..." -ForegroundColor Cyan
            $env:PYTHONPATH = "$env:APPDATA\Python\Python312\site-packages"
            streamlit run output/dashboard.py
        }
        "3" {
            Clear-Host
            Write-Host "[*] Running Test Suite..." -ForegroundColor Cyan
            pytest tests/ -v
            Write-Host "`nPress any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "4" {
            Clear-Host
            Write-Host "[*] Starting Docker Containers..." -ForegroundColor Cyan
            docker compose up -d
            Write-Host "`nNeo4j Browser: http://localhost:7474 (neo4j / password)" -ForegroundColor Green
            Write-Host "Vault Web UI:  http://localhost:8200 (token: root)" -ForegroundColor Green
            Write-Host "`nPress any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "5" {
            Clear-Host
            Write-Host "[*] Stopping Docker Containers..." -ForegroundColor Yellow
            docker compose down
            Write-Host "`nPress any key to return to menu..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        "6" {
            Write-Host "Goodbye!" -ForegroundColor Cyan
            break
        }
        default {
            Write-Host "Invalid choice. Please choose 1-6." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "6")
