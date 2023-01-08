-- Se imputa nulo a los valores -999 en el campo altura
UPDATE accidentes_no 
SET altitud = NULL
WHERE altitud = -999;

-- Se imputa nulo a los valores -9999 en el campo pendiente
UPDATE accidentes_no 
SET pendiente = NULL
WHERE pendiente = -9999;