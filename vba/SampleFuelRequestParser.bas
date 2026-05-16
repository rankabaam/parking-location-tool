Option Explicit

' SampleFuelRequestParser.bas
'
' This is a sanitized portfolio demo module.
' It uses fictional sample fuel request text only.
' No real company data, aircraft records, employee names, or internal procedures are included.

Public Sub Demo_ParseSampleFuelRequests()

    Dim sampleBodies(1 To 3) As String
    Dim i As Long

    sampleBodies(1) = _
        "Aircraft: N123AB" & vbCrLf & _
        "Ramp: Ramp A" & vbCrLf & _
        "Spot: 4" & vbCrLf & _
        "Fuel Type: 100LL" & vbCrLf & _
        "Requested Time: 2026-05-15 07:32"

    sampleBodies(2) = _
        "Aircraft: N456CD" & vbCrLf & _
        "Ramp: Ramp B" & vbCrLf & _
        "Spot: 2" & vbCrLf & _
        "Fuel Type: Jet A" & vbCrLf & _
        "Requested Time: 2026-05-15 07:41"

    sampleBodies(3) = _
        "Aircraft: N789EF" & vbCrLf & _
        "Ramp: Ramp C" & vbCrLf & _
        "Spot: 8" & vbCrLf & _
        "Fuel Type: 100LL" & vbCrLf & _
        "Requested Time: 2026-05-15 08:05"

    Debug.Print "tail_number,ramp,spot,fuel_type,request_time"

    For i = LBound(sampleBodies) To UBound(sampleBodies)
        Debug.Print _
            ExtractField(sampleBodies(i), "Aircraft:") & "," & _
            ExtractField(sampleBodies(i), "Ramp:") & "," & _
            ExtractField(sampleBodies(i), "Spot:") & "," & _
            ExtractField(sampleBodies(i), "Fuel Type:") & "," & _
            ExtractField(sampleBodies(i), "Requested Time:")
    Next i

End Sub

Private Function ExtractField(ByVal bodyText As String, ByVal fieldLabel As String) As String

    Dim lines() As String
    Dim lineText As Variant
    Dim valueText As String

    lines = Split(bodyText, vbCrLf)

    For Each lineText In lines
        If LCase(Left(Trim(CStr(lineText)), Len(fieldLabel))) = LCase(fieldLabel) Then
            valueText = Trim(Mid(CStr(lineText), Len(fieldLabel) + 1))
            ExtractField = valueText
            Exit Function
        End If
    Next lineText

    ExtractField = ""

End Function
