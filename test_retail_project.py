from lib.DataReader import read_customers, read_orders
from lib.DataManupulation import filter_closed_orders, count_orders_state
from lib.ConfigReader import get_app_conf
import pytest

def test_read_customers_df(spark):
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count == 12435


def test_read_orders_df(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884
    
@pytest.mark.transformation
def test_filter_closed_orders(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_closed_orders(orders_df).count()
    assert filtered_count == 7556
    
@pytest.mark.skip(reason="Work in Progress")
def test_read_app_config():
    config = get_app_conf("LOCAL")
    assert config['orders.file.path'] == "data/orders.csv"
    
@pytest.mark.transformation
def test_count_orders_state(spark, expected_results):
    customers_df = read_customers(spark, "LOCAL")
    actual_results = count_orders_state(customers_df)
    assert actual_results.collect() == expected_results.collect()