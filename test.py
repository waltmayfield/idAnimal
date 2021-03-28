numPredictionsHonored = 10
LastXTracker = [("dummy",0)]*numPredictionsHonored

print(len(LastXTracker))

LastXTracker = [('Freddy', 0.99)] + LastXTracker[0:-1]

print(len(LastXTracker))
