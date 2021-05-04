Remove-Item -Path ./combined.css

$mobileScripts = Get-ChildItem -Path  . -Filter "mobile*.css" -Exclude "*master.css", "*outsourced.css" -Recurse
$defaultScripts = Get-ChildItem -Path  . -Filter "*.css" -Exclude "mobile*.css", "master.css", "outsourced.css" -Recurse

$names = @("mobile_combined.css", "combined.css")
$scripts = @($mobileScripts, $defaultScripts)

Write-Output $name, $args[0], ($args[0] -eq "-m")

for ( $i = 0; $i -lt 2; $i++ ) {
  New-Item -Path . -Name $names[$i] -ItemType "file" -Value "" -Force
  foreach ($script in $scripts[$i]) {
    $content = Get-Content -Path $script.FullName
    Add-Content -Path ./combined.css -Value "/* Styles from: $($script.Name) */"
    Add-Content -Path ./combined.css -Value $content
  }
}