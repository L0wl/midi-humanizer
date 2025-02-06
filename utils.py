from mido import *
import random

class LogicHandler:
    @staticmethod
    def humanizeMidi(mid, trackParams: dict):
        newMidi = MidiFile(ticks_per_beat=mid.ticks_per_beat)
        for trackIndex, track in enumerate(mid.tracks):
            newTrack = MidiTrack()
            newMidi.tracks.append(newTrack)
            
            params: dict = trackParams.get(trackIndex, None)
            
            if params is None: continue

            timeRange: int = params.get("timeRange", 0)
            durationRange: int = params.get("durationRange", 0)
            velocityRange: int = params.get("velocityRange", 0)
            durationPrecentage: float = params.get("durationPrecent", 0.0)

            absTime = 0
            events = []
            for msg in track:
                absTime += msg.time
                events.append({"absTime": absTime, "msg": msg})
            
            activeNotes = {}
            processedEvents = []
            for event in events:
                msg = event["msg"]
                if msg.type == "note_on" and msg.velocity > 0:
                    key = (msg.channel, msg.note)
                    activeNotes[key] = event
                elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                    key = (msg.channel, msg.note)
                    if key in activeNotes:
                        note_on = activeNotes.pop(key)
                        note_off = event

                        originalDuration = note_off["absTime"] - note_on["absTime"]
                        reducedDuration = int(originalDuration * (1 - durationPrecentage / 100.0))
                        note_off["absTime"] = note_on["absTime"] + reducedDuration

                        timeOffset = random.randint(0, timeRange)
                        durationOffset = random.randint(-timeRange, durationRange)
                        velocityOffset = random.randint(-timeRange, velocityRange)

                        note_on["absTime"] += timeOffset
                        note_off["absTime"] += timeOffset
                        note_off["absTime"] += durationOffset

                        if note_on["absTime"] >= note_off["absTime"]:
                            note_off['absTime'] = note_on['absTime'] + 1
                        
                        newVelocity = note_on["msg"].velocity + velocityOffset
                        note_on["msg"] = note_on["msg"].copy(velocity=min(max(newVelocity, 1), 127))
                        processedEvents.extend([note_on, note_off])
                    else:
                        processedEvents.append(event)
                else:
                    processedEvents.append(event)
            
            processedEvents.sort(key=lambda x: x["absTime"])
            lastTime = 0

            for event in processedEvents:
                delta = event["absTime"] - lastTime
                newMsg = event['msg'].copy(time=delta)
                newTrack.append(newMsg)
                lastTime = event['absTime']
        return newMidi