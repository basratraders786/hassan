from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class FuelTank:
    """Store fuel level and pricing for one fuel type."""

    name: str
    price_per_liter: float
    quantity_liters: float

    def refill(self, liters: float) -> None:
        if liters <= 0:
            raise ValueError("Refill liters must be greater than zero.")
        self.quantity_liters += liters

    def sell(self, liters: float) -> float:
        if liters <= 0:
            raise ValueError("Sale liters must be greater than zero.")
        if liters > self.quantity_liters:
            raise ValueError(
                f"Insufficient stock in {self.name}. Available: {self.quantity_liters:.2f} L"
            )
        self.quantity_liters -= liters
        return liters * self.price_per_liter


@dataclass
class SaleRecord:
    fuel_type: str
    liters: float
    amount: float
    payment_mode: str
    timestamp: datetime = field(default_factory=datetime.now)


class PetrolPumpSoftware:
    """Simple petrol pump management system for stock + sales tracking."""

    def __init__(self) -> None:
        self.tanks: Dict[str, FuelTank] = {
            "petrol": FuelTank("Petrol", 104.0, 5000.0),
            "diesel": FuelTank("Diesel", 92.0, 8000.0),
            "cng": FuelTank("CNG", 78.0, 3000.0),
        }
        self.sales: List[SaleRecord] = []

    def update_price(self, fuel_key: str, new_price: float) -> None:
        tank = self._get_tank(fuel_key)
        if new_price <= 0:
            raise ValueError("Price must be greater than zero.")
        tank.price_per_liter = new_price

    def refill_tank(self, fuel_key: str, liters: float) -> None:
        tank = self._get_tank(fuel_key)
        tank.refill(liters)

    def record_sale(self, fuel_key: str, liters: float, payment_mode: str) -> SaleRecord:
        tank = self._get_tank(fuel_key)
        amount = tank.sell(liters)
        sale = SaleRecord(tank.name, liters, amount, payment_mode)
        self.sales.append(sale)
        return sale

    def total_revenue(self) -> float:
        return sum(s.amount for s in self.sales)

    def total_liters_sold(self) -> float:
        return sum(s.liters for s in self.sales)

    def fuel_wise_sales(self) -> Dict[str, float]:
        result: Dict[str, float] = {t.name: 0.0 for t in self.tanks.values()}
        for sale in self.sales:
            result[sale.fuel_type] += sale.liters
        return result

    def status_report(self) -> str:
        lines = ["\n=== PETROL PUMP STATUS REPORT ==="]
        for tank in self.tanks.values():
            lines.append(
                f"{tank.name:7} | Price: ₹{tank.price_per_liter:.2f}/L | Stock: {tank.quantity_liters:.2f} L"
            )
        lines.append(f"Total Sales Transactions: {len(self.sales)}")
        lines.append(f"Total Liters Sold: {self.total_liters_sold():.2f} L")
        lines.append(f"Total Revenue: ₹{self.total_revenue():.2f}")

        lines.append("\nFuel Wise Sales:")
        for fuel, liters in self.fuel_wise_sales().items():
            lines.append(f"- {fuel}: {liters:.2f} L")
        return "\n".join(lines)

    def _get_tank(self, fuel_key: str) -> FuelTank:
        key = fuel_key.strip().lower()
        if key not in self.tanks:
            valid = ", ".join(self.tanks.keys())
            raise ValueError(f"Invalid fuel type '{fuel_key}'. Use: {valid}")
        return self.tanks[key]


def run_cli() -> None:
    software = PetrolPumpSoftware()

    menu = """
====== PETROL PUMP SOFTWARE ======
1. Sell Fuel
2. Refill Tank
3. Update Fuel Price
4. View Report
5. Exit
Choose option: """

    while True:
        try:
            choice = input(menu).strip()

            if choice == "1":
                fuel = input("Fuel type (petrol/diesel/cng): ")
                liters = float(input("Liters to sell: "))
                payment = input("Payment mode (cash/card/upi): ")
                sale = software.record_sale(fuel, liters, payment)
                print(
                    f"Sale successful: {sale.liters:.2f} L {sale.fuel_type} | Bill ₹{sale.amount:.2f}"
                )

            elif choice == "2":
                fuel = input("Fuel type (petrol/diesel/cng): ")
                liters = float(input("Liters to refill: "))
                software.refill_tank(fuel, liters)
                print("Tank refilled successfully.")

            elif choice == "3":
                fuel = input("Fuel type (petrol/diesel/cng): ")
                new_price = float(input("New price per liter: ₹"))
                software.update_price(fuel, new_price)
                print("Price updated successfully.")

            elif choice == "4":
                print(software.status_report())

            elif choice == "5":
                print("Dhanyavaad! Petrol pump software बंद हो रहा है.")
                break

            else:
                print("Invalid option. Please choose 1-5.")

        except ValueError as error:
            print(f"Error: {error}")


def run_preview() -> None:
    """Run a short non-interactive preview so users can quickly see output."""
    software = PetrolPumpSoftware()
    software.record_sale("petrol", 5, "cash")
    software.record_sale("diesel", 7.5, "upi")
    software.refill_tank("cng", 100)
    print(software.status_report())


def main() -> None:
    parser = argparse.ArgumentParser(description="Petrol Pump Software")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Run non-interactive preview (demo report) instead of opening menu.",
    )
    args = parser.parse_args()

    if args.preview:
        run_preview()
    else:
        run_cli()


if __name__ == "__main__":
    main()
