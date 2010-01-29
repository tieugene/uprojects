; AddonCD menu
; menu is in menu.lst:
; default <tab> exec <tab> Name
;#include "GuiConstantsEx.au3"

; Events and messages
Global Const $GUI_EVENT_CLOSE = -3
Global Const $GUI_CHECKED = 1
Global Const $GUI_UNCHECKED = 4
Global Const $ASize = 50

Global $Array[$ASize][4]

; 0. GUI
GuiCreate("Menu", 250, 400)
$ButtonD = GuiCtrlCreateButton("Default", 0, 0, 50, 25)
GUICtrlSetOnEvent($ButtonD, "OnDefault")
$ButtonA = GuiCtrlCreateButton("All", 50, 0, 50, 25)
GUICtrlSetOnEvent($ButtonA, "OnAll")
$ButtonN = GuiCtrlCreateButton("None", 100, 0, 50, 25)
GUICtrlSetOnEvent($ButtonN, "OnNone")
$ButtonX = GuiCtrlCreateButton("Do it!", 150, 0, 50, 25)
GUICtrlSetOnEvent($ButtonX, "OnDoit")
$ButtonQ = GuiCtrlCreateButton("Exit", 200, 0, 50, 25)
GUICtrlSetOnEvent($ButtonQ, "OnExit")

; 1. Load data
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
	If $linearray[0] = "" Then
		$Array[$i][0] = false
	Else
		$Array[$i][0] = true
	EndIf
	$Array[$i][1] = $linearray[1]
	$Array[$i][2] = $linearray[2]
	$i = $i + 1
Wend
FileClose($file)
Global $RSize = $i

; 3. CHECKBOX
For $i = 0 To $RSize-1
	$Array[$i][3] = GuiCtrlCreateCheckbox($Array[$i][2], 0, 25 + $i * 20)
Next
setDefaults($Array)

; 4. GUI MESSAGE LOOP
GuiSetState()
Do
	$msg = GUIGetMsg()
	Select
		Case $msg = $ButtonD
			setDefaults($Array)
		Case $msg = $ButtonA
			setAll($Array, $GUI_CHECKED)
		Case $msg = $ButtonN
			setAll($Array, $GUI_UNCHECKED)
	EndSelect
Until $msg = $GUI_EVENT_CLOSE Or $msg = $ButtonQ

Func setDefaults($a)
	For $i = 0 To $RSize-1
		If $a[$i][0] = true Then
			GuiCtrlSetState($a[$i][3], $GUI_CHECKED)
		Else
			GuiCtrlSetState($a[$i][3], $GUI_UNCHECKED)
		Endif
	Next
EndFunc

Func setAll($a, $state)
	For $i = 0 To $RSize-1
		GuiCtrlSetState($a[$i][3], $state)
	Next
EndFunc
