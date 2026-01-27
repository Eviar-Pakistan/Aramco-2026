# Path to your user file and Django manage.py
$userFile = "D:\EviarWork\Aramco\Aramco\coco_aramco_users.txt"
$projectPath = "D:\EviarWork\Aramco\Aramco"

# Change directory to Django project folder
Set-Location $projectPath

Get-Content $userFile | ForEach-Object {
    if ($_ -match 'username: ([^,]+), password: ([^ ]+)\s+\|\|\s+Location: (.+)$') {
        $username = $Matches[1]
        $password = $Matches[2]
        #$location = $Matches[3]  # Uncomment if needed
        $pythonCommand = @"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$username').exists():
    user = User.objects.create_user(
        username='$username',
        password='$password',
        is_superuser=False,
        is_staff=False,
        is_active=True,
    )
    user.save()
"@
        $pythonCommand | & python manage.py shell
    }
}
Write-Host "All users imported."