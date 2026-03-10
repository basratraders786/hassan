# Petrol Pump Software

Yeh ek simple Python-based petrol pump management software hai.
Isme aap fuel sale, tank refill, fuel price update aur report dekh sakte ho.

## Features
- Petrol, Diesel, CNG ka stock manage karna
- Sale entry + automatic bill calculation
- Payment mode capture (cash/card/upi)
- Fuel refill and price updates
- Revenue + liters sold summary report

## Run
```bash
python3 petrol_pump_software.py
```

## Preview (without menu)
Agar aapko jaldi se output dekhna ho (interactive inputs ke baghair), yeh command chalao:

```bash
python3 petrol_pump_software.py --preview
```

Is se sample sales/refill run hoga aur status report print ho jayegi.

## Test
```bash
python3 -m pytest -q
```
