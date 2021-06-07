Remove-Item -Path ./combined.css

$allscripts = Get-ChildItem -Path  . -Filter "*.css" -Exclude "master.css", "outsourced.css" -Recurse

New-Item -Path . -Name "combined.css" -ItemType "file" -Value ""
foreach ($script in $allscripts) {
  $content = Get-Content -Path $script.FullName
  Add-Content -Path ./combined.css -Value "/* Styles from: $($script.Name) */"
  Add-Content -Path ./combined.css -Value $content
}