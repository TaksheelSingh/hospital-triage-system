"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Sidebar } from "@/components/hospital/sidebar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { User, Ambulance, Activity, Heart, FileText, Send } from "lucide-react"
import type { StaffFormStatus } from "@/lib/hospital-data"
import { staffFormStatusInfo } from "@/lib/hospital-data"

export default function StaffDashboard() {
  const [formStatus, setFormStatus] = useState<StaffFormStatus>("idle")
  const [ambulanceTransfer, setAmbulanceTransfer] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [arrivalTime, setArrivalTime] = useState("")
  const [hasInput, setHasInput] = useState(false)

  useEffect(() => {
    const updateTime = () => {
      const now = new Date()
      const hours = String(now.getHours()).padStart(2, "0")
      const minutes = String(now.getMinutes()).padStart(2, "0")
      setArrivalTime(`${hours}:${minutes}`)
    }

    updateTime()
    const interval = setInterval(updateTime, 1000)

    return () => clearInterval(interval)
  }, [])

  const handleInputChange = () => {
    if (!hasInput && formStatus === "idle") {
      setFormStatus("in-progress")
      setHasInput(true)
    }
  }

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  setIsSubmitting(true)

  try {
    // 1️⃣ Create Patient
    const patientRes = await fetch("http://127.0.0.1:8000/patients", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: (document.getElementById("name") as HTMLInputElement)?.value,
        age: Number((document.getElementById("age") as HTMLInputElement)?.value),
        gender: "Other",
        email: (document.getElementById("email") as HTMLInputElement)?.value,
        phone: (document.getElementById("phone") as HTMLInputElement)?.value,
      }),
    })

    const patientData = await patientRes.json()

    // 2️⃣ Create Visit + Predict
    await fetch("http://127.0.0.1:8000/visits/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        patient_id: patientData.id,
        arrival_mode: "Other",
        ambtransfer: ambulanceTransfer,
        arrival_time: arrivalTime + ":00",
        temperature: Number((document.getElementById("temp") as HTMLInputElement)?.value),
        pulse: Number((document.getElementById("pulse") as HTMLInputElement)?.value),
        respiration: Number((document.getElementById("respiration") as HTMLInputElement)?.value),
        systolic_bp: Number((document.getElementById("bp-systolic") as HTMLInputElement)?.value),
        diastolic_bp: Number((document.getElementById("bp-diastolic") as HTMLInputElement)?.value),
        pain_scale: Number((document.getElementById("pain") as HTMLInputElement)?.value),
        rfv1: null,
        rfv2: null,
        rfv3: null,
        rfv_text: (document.getElementById("rfv1") as HTMLInputElement)?.value,
      }),
    })

    setFormStatus("submitted")
    alert("Patient Registered Successfully")

  } catch (err) {
    console.error(err)
    alert("Submission Failed")
  }

  setIsSubmitting(false)
}

  const handleReset = () => {
    setFormStatus("idle")
    setHasInput(false)
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <main className="ml-64 min-h-screen">
        <header className="sticky top-0 z-30 border-b bg-card/80 backdrop-blur-sm">
          <div className="flex h-16 items-center justify-between px-6">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">Patient Intake Portal</h1>
              <p className="text-sm text-muted-foreground">Staff Dashboard - Register new patients</p>
            </div>
            <Badge className={staffFormStatusInfo[formStatus].badgeColor}>
              {staffFormStatusInfo[formStatus].label}
            </Badge>
          </div>
        </header>

        <form onSubmit={handleSubmit} className="p-6">
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Patient Info */}
            <Card className="lg:col-span-2">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <User className="h-5 w-5 text-primary" />
                  Patient Information
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 grid-cols-3">
                  <div className="space-y-2">
                    <Label htmlFor="name">Patient Name</Label>
                    <Input id="name" placeholder="Full name" onChange={handleInputChange} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone</Label>
                    <Input id="phone" type="tel" placeholder="Contact number" onChange={handleInputChange} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="Email address" onChange={handleInputChange} />
                  </div>
                </div>
                <div className="grid gap-4 grid-cols-3">
                  <div className="space-y-2">
                    <Label htmlFor="age">Age</Label>
                    <Input id="age" type="number" min={0} max={150} onChange={handleInputChange} />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="sex">Sex</Label>
                    <Select onValueChange={handleInputChange}>
                      <SelectTrigger id="sex">
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="dov">Date of Visit</Label>
                    <Input id="dov" type="date" onChange={handleInputChange} />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Arrival Details */}
            <Card className="lg:col-span-1">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Ambulance className="h-5 w-5 text-primary" />
                  Arrival Details
                </CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="arrems">Arrival Mode</Label>
                  <Select>
                    <SelectTrigger id="arrems">
                      <SelectValue placeholder="Select mode" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="walk-in">Walk-in</SelectItem>
                      <SelectItem value="ambulance">Ambulance</SelectItem>
                      <SelectItem value="private-vehicle">Private Vehicle</SelectItem>
                      <SelectItem value="police">Police Transport</SelectItem>
                      <SelectItem value="helicopter">Helicopter</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="arrtime">Arrival Time</Label>
                  <Input id="arrtime" type="time" value={arrivalTime} readOnly className="bg-muted" />
                </div>
              </CardContent>
            </Card>

            {/* Ambulance Transfer */}
            <Card>
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Activity className="h-5 w-5 text-primary" />
                  Transfer Details
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between rounded-lg border p-4">
                  <div className="space-y-0.5">
                    <Label htmlFor="ambulance">Ambulance Transfer</Label>
                    <p className="text-sm text-muted-foreground">Patient arrived via ambulance transfer</p>
                  </div>
                  <Switch id="ambulance" checked={ambulanceTransfer} onCheckedChange={(checked) => {
                    setAmbulanceTransfer(checked)
                    handleInputChange()
                  }} />
                </div>
              </CardContent>
            </Card>

            {/* Vitals Entry */}
            <Card>
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Heart className="h-5 w-5 text-primary" />
                  Vitals Entry
                </CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="temp">Temperature (°F)</Label>
                  <Input id="temp" type="number" step="0.1" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pulse">Pulse (bpm)</Label>
                  <Input id="pulse" type="number" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="respiration">Respiration Rate</Label>
                  <Input id="respiration" type="number" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="bp-systolic">BP Systolic</Label>
                  <Input id="bp-systolic" type="number" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="bp-diastolic">BP Diastolic</Label>
                  <Input id="bp-diastolic" type="number" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pain">Pain Scale (0-10)</Label>
                  <Input id="pain" type="number" min={0} max={10} />
                </div>
              </CardContent>
            </Card>

            {/* Reason for Visit */}
            <Card className="lg:col-span-2">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-lg">
                  <FileText className="h-5 w-5 text-primary" />
                  Reason for Visit
                </CardTitle>
              </CardHeader>
              <CardContent className="grid gap-4 sm:grid-cols-3">
                <div className="space-y-2">
                  <Label htmlFor="rfv1">Primary Reason</Label>
                  <Input id="rfv1" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rfv2">Secondary Reason</Label>
                  <Input id="rfv2" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="rfv3">Tertiary Reason</Label>
                  <Input id="rfv3" />
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="mt-6 flex justify-end gap-4">
            <Button type="button" variant="outline" onClick={handleReset}>
              Clear Form
            </Button>
            <Button type="submit" size="lg" className="min-w-[200px]" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <span className="animate-spin mr-2">
                    <Activity className="h-5 w-5" />
                  </span>
                  Processing...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-5 w-5" />
                  Submit Patient Record
                </>
              )}
            </Button>
          </div>
        </form>
      </main>
    </div>
  )
}
