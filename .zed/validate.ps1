
$filePath = $Env:ZED_FILE
$ddsclient = New-Object -ComObject "CxDds.DdsClient"
$ddsclient.Connect("CENTRAL.DDS")
$uisclient = New-Object -ComObject "CxUis.UisClient"
$uisclient.Connect("CENTRAL.UIS")

$ddsclient.ValidateDevTemplateFromFile($filePath)
$ddsclient.InstallDevTemplateFromFile($filePath)

#$uisclient.SendUISCommand("WL_MN_02_CTL_RD","DG_T_DEV",'DataType=i4;DGORD=0;DGTYPE=SnglRegRw;RegNum=20;Value=7',"")


$ddsclient.Disconnect()
$uisclient.Disconnect()
