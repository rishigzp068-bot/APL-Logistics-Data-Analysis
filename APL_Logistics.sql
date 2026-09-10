CREATE DATABASE apl_logistics;
USE apl_logistics;

describe logistics_data;


SELECT COUNT(*) AS total_rows
from logistics_data;


SELECT 
    AVG(`Days for shipping (real)`) AS avg_actual_shipping_days,
    AVG(`Days for shipment (scheduled)`) AS avg_scheduled_shipping_days
FROM logistics_data;



SELECT
    Late_delivery_risk,
    COUNT(*) AS Order_Count
FROM logistics_data
GROUP BY Late_delivery_risk;

select
count(*) as total_orders,
sum(case
when late_delivery_risk =1 then 1
else 0
end) as late_orders,
round(
100.0 * sum(case
when late_delivery_risk = 1 then 1
else 0
end) / count(*),
2
) as late_delivery_percentage
from logistics_data;

SELECT
    `Shipping Mode`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY `Shipping Mode`
ORDER BY Late_Delivery_Rate DESC;


SELECT
    `Order Region`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY `Order Region`
ORDER BY Late_Delivery_Rate DESC;



SELECT
    Market,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN Late_delivery_risk = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        100.0 * AVG(CAST(Late_delivery_risk AS DECIMAL(10,4))),
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY Market
ORDER BY Late_Delivery_Rate DESC;



SELECT
    `Customer Segment`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Order Profit Per Order`), 2) AS Total_Profit
FROM logistics_data
GROUP BY `Customer Segment`
ORDER BY Late_Delivery_Rate DESC;



SELECT
    `Order Item Quantity`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY `Order Item Quantity`
ORDER BY `Order Item Quantity`;



SELECT
    `Order Item Quantity`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY `Order Item Quantity`
ORDER BY `Order Item Quantity`;



SELECT
    `Days for shipment (scheduled)`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY `Days for shipment (scheduled)`
ORDER BY `Days for shipment (scheduled)`;



SELECT
    `Late_delivery_risk`,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(`Sales`), 2) AS Total_Sales,
    ROUND(SUM(`Order Profit Per Order`), 2) AS Total_Profit
FROM logistics_data
GROUP BY `Late_delivery_risk`
ORDER BY `Late_delivery_risk`;


SELECT
    `Order Region`,
    `Shipping Mode`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY
    `Order Region`,
    `Shipping Mode`
ORDER BY
    Late_Delivery_Rate DESC;
    
    
    SELECT
    `Order Region`,
    `Shipping Mode`,
    COUNT(*) AS Total_Orders,
    SUM(CASE
        WHEN `Late_delivery_risk` = 1 THEN 1
        ELSE 0
    END) AS Late_Orders,
    ROUND(
        AVG(`Late_delivery_risk`) * 100,
        2
    ) AS Late_Delivery_Rate
FROM logistics_data
GROUP BY
    `Order Region`,
    `Shipping Mode`
HAVING COUNT(*) >= 50
ORDER BY
    Late_Delivery_Rate DESC;
    
    