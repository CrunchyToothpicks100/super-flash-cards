# Flash Cards - Temporary Session Aliases
# Usage: . .\activate_aliases.ps1

$ProjectRoot = $PSScriptRoot

function newset         { python "$ProjectRoot\main.py" newset @args }
function select-set    { python "$ProjectRoot\main.py" select @args }
function create         { python "$ProjectRoot\main.py" create @args }
function show           { python "$ProjectRoot\main.py" show @args }
function flip           { python "$ProjectRoot\main.py" flip @args }
function scrape         { python "$ProjectRoot\main.py" scrape @args }
function autogen           { python "$ProjectRoot\main.py" autogenerate @args }
function delete-set        { python "$ProjectRoot\main.py" delete @args }

Write-Host "Flash card aliases loaded for this session:"
Write-Host "  newset    - Create a new flash card set"
Write-Host "  select-set    - Select an existing set"
Write-Host "  create    - Add a flash card to the current set"
Write-Host "  show      - Show a random flash card"
Write-Host "  flip      - Flip the last shown card"
Write-Host "  scrape    - Scrape web/page.html"
Write-Host "  autogen      - Autogenerate a set (args: <output_name> [--model <name>])"
Write-Host "  delete-set   - Delete the currently selected set"
