; AddonCD menu
; menu is in menu.lst:
; default <tab> exec <tab> Name

; 0. Constants
Global Const $GUI_EVENT_CLOSE = -3
Global Const $GUI_CHECKED = 1
Global Const $GUI_UNCHECKED = 4
Global Const $TVS_CHECKBOXES = 0x00000100 ; Enables check boxes for items

; 1. Vars
Global $CmdAuto = "cmd.auto"
Global Const $ASize = 50
Global $Array[$ASize][3]	; defaultflag|exec|guicontrol

; 3. GUI
GuiCreate("AddOnCD", 250, 400)
$MenuSelect		= GuiCtrlCreateMenu("&Select")
$ActionDefault		= GuiCtrlCreateMenuItem("&Default", $MenuSelect)
$ActionSelectAll	= GuiCtrlCreateMenuItem("A&ll", $MenuSelect)
$ActionSelectNone	= GuiCtrlCreateMenuItem("&None", $MenuSelect)
$MenuMode		= GuiCtrlCreateMenu("&Go mode")
$ActionModeAuto		= GuiCtrlCreateMenuItem("&Auto", $MenuMode)
$ActionModeRaw		= GuiCtrlCreateMenuItem("&Raw", $MenuMode)
$ActionGo		= GuiCtrlCreateButton("&Go!", 0, 0, 50, 20)
$ActionExit		= GuiCtrlCreateButton("E&xit", 50, 0, 50, 20)

$tree = GuiCtrlCreateTreeView(0, 20, 250, 350, $TVS_CHECKBOXES)

; 4. Load data && set items
$file = FileOpen("menu.lst", 0)
If $file = -1 Then
	MsgBox(0, "Error", "Unable to open menu.lst.")
	Exit
EndIf
$i = 0
While 1
	$line = FileReadLine($file)
	If @error = -1 Then ExitLoop
	$linearray = StringSplit ($line, @TAB, 2)
	$filepath = $CmdAuto & "\" & $linearray[1]
	If FileExists($filepath) Then
		If $linearray[0] = "" Then
			$Array[$i][0] = false
		Else
			$Array[$i][0] = true
		EndIf
		;$Array[$i][1] = $linearray[1]
		$Array[$i][1] = $filepath
		$Array[$i][2] = GuiCtrlCreateTreeViewItem($linearray[2], $tree)
		$i = $i + 1
	EndIf
Wend
FileClose($file)

Global $RSize = $i
setDefaults($Array)

; 4. GUI MESSAGE LOOP
GuiSetState()
Do
	$msg = GUIGetMsg()
	Select
		Case $msg = $ActionDefault
			setDefaults($Array)
		Case $msg = $ActionSelectAll
			setAll($Array, $GUI_CHECKED)
		Case $msg = $ActionSelectNone
			setAll($Array, $GUI_UNCHECKED)
		Case $msg = $ActionGo
			For $i = 0 To $RSize-1
				$state = BitAND(GuiCtrlRead($Array[$i][2]), 7)
				;MsgBox(0, "Item", $Array[$i][1])
				;MsgBox(0, "State", $state)
				If $state = 1 Then
					;MsgBox(0, "Item", $Array[$i][1])
					RunWait($Array[$i][1])
				EndIf
			Next
	EndSelect
Until $msg = $GUI_EVENT_CLOSE Or $msg = $ActionExit

; X. funcs
Func setDefaults($a)
	For $i = 0 To $RSize-1
		If $a[$i][0] = true Then
			GuiCtrlSetState($a[$i][2], $GUI_CHECKED)
		Else
			GuiCtrlSetState($a[$i][2], $GUI_UNCHECKED)
		Endif
	Next
EndFunc

Func setAll($a, $state)
	For $i = 0 To $RSize-1
		GuiCtrlSetState($a[$i][2], $state)
	Next
EndFunc
