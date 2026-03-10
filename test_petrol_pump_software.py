from petrol_pump_software import PetrolPumpSoftware, run_preview


def test_record_sale_reduces_stock_and_adds_revenue() -> None:
    app = PetrolPumpSoftware()
    initial_stock = app.tanks["petrol"].quantity_liters

    sale = app.record_sale("petrol", 10, "cash")

    assert sale.amount == 10 * 104.0
    assert app.tanks["petrol"].quantity_liters == initial_stock - 10
    assert app.total_revenue() == sale.amount


def test_refill_increases_stock() -> None:
    app = PetrolPumpSoftware()
    initial_stock = app.tanks["diesel"].quantity_liters

    app.refill_tank("diesel", 120)

    assert app.tanks["diesel"].quantity_liters == initial_stock + 120


def test_invalid_fuel_raises_error() -> None:
    app = PetrolPumpSoftware()

    try:
        app.record_sale("water", 10, "cash")
        assert False, "Expected ValueError"
    except ValueError as err:
        assert "Invalid fuel type" in str(err)


def test_preview_prints_status_report(capsys) -> None:
    run_preview()
    output = capsys.readouterr().out
    assert "PETROL PUMP STATUS REPORT" in output
    assert "Total Revenue" in output
