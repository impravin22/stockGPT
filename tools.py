from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
import requests
import json
import openai

def check_real_price(stock_symbol):
    url = "https://twelve-data1.p.rapidapi.com/price"

    querystring = {"symbol": stock_symbol, "format": "json", "outputsize": "30"}

    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }



    response = requests.get(url, headers=headers, params=querystring)

    json_response = response.json()

    return json_response["price"]
    # return json_response["volume"]


def check_week_volume(stock_symbol):
    print(f"Function calling: Check for stock {stock_symbol}")

    url = "https://twelve-data1.p.rapidapi.com/quote"

    querystring = {
        "symbol": stock_symbol,
        "interval": "1week",
        "outputsize": "30",
        "format": "json",
    }

    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print("stock rsponse of volume: ", response.json()["volume"])
    print(response.json())
    return response.json()["volume"]

def check_month_volume(stock_symbol):
    print(f"Function calling: Check for stock {stock_symbol}")

    url = "https://twelve-data1.p.rapidapi.com/quote"

    querystring = {
        "symbol": stock_symbol,
        "interval": "1month",
        "outputsize": "30",
        "format": "json",
    }

    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print("stock rsponse of volume: ", response.json()["volume"])
    print(response.json())
    return response.json()["volume"]

def check_30min_volume(stock_symbol):
    print(f"Function calling: Check for stock {stock_symbol}")

    url = "https://twelve-data1.p.rapidapi.com/quote"

    querystring = {
        "symbol": stock_symbol,
        "interval": "30min",
        "outputsize": "30",
        "format": "json",
    }

    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print("stock rsponse of volume: ", response.json()["volume"])
    print(response.json())
    return response.json()["volume"], response.json()["average_volume"]

def check_stock_symbol(stock_symbol):
    print(f"Function calling: Check for stock {stock_symbol}")

    url = "https://twelve-data1.p.rapidapi.com/quote"

    querystring = {
        "symbol": stock_symbol,
        "interval": "30min",
        "outputsize": "30",
        "format": "json",
    }

    headers = {
        "X-RapidAPI-Key": "your_api_key",
        "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    print("stock rsponse of volume: ", response.json()["volume"])
    print(response.json())
    return response.json()

#
# explanation_prompt = f"""
#     You are an expert of volume spread analysis. Given that the financial quote on volume
#     information of this stock during the previous 30 minutes is {thrity_volume}, for the
#     past 1 week is {week_volume}, and for the past 1 month is {month_volume}, produce recommended
#     action for this stock.
#
# """

def get_stock_recommendation(thirty_volume, avg_volume, month_volume, week_volume, stock_quote):
    explanation_prompt = f"""
    You are an expert of volume spread analysis. Given that the financial quote on volume 
    information of this stock during the previous 30 minutes is {thirty_volume} where as the
    average volume is {avg_volume}, for the 
    past 1 week is {week_volume}, and for the past 1 month is {month_volume}, produce recommended
    action for this stock for today, and this week.
    Your choices are strong sell, moderate sell, neutral, moderate buy, or strong buy. 
    Provide the reasoning behind your choice as well.

    """
    explanation_prompt += json.dumps(stock_quote)
    openai.api_key = "your_api_key"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.1,
        messages=[
            {
                "role": "user",
                "content": explanation_prompt,
            },
        ],
    )

    return response
# def get_stock_recommendation(current_price, stock_quote):
#     explanation_prompt = f"""
#     Given that the current price of this stock is {current_price} and the financial quote information
#     during the previous 30 minutes provided below, produce recommended action for this stock.
#     Your choices are strong sell, moderate sell, neutral, moderate buy, or strong buy.
#     Provide the reasoning behind your choice as well.
#
#     """
#     explanation_prompt += json.dumps(stock_quote)
#     openai.api_key = "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"
#
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         temperature=0.1,
#         messages=[
#             {
#                 "role": "user",
#                 "content": explanation_prompt,
#             },
#         ],
#     )
#
#     return response


class InvestingAdvisorCheckInput(BaseModel):
    stock_symbol: str = Field(
        ..., description="The symbol of stock to be searched. For instance: AAPL, AMZN"
    )


class InvestingAdvisorTool(BaseTool):
    name = "check_stock_symbol"
    description = """
    Use this tool when you need to check whether it is a good time to buy a certain stock or not.
    This tool should only be used to check 1 stock name at a time.
    """

    def _run(self, stock_symbol: str):
        real_30min_volume, avg_volume = check_30min_volume(stock_symbol=stock_symbol)
        real_week_volume = check_week_volume(stock_symbol=stock_symbol)
        real_month_volume = check_month_volume(stock_symbol=stock_symbol)
        print("30min volume is: ", real_30min_volume)
        print("week volume is: ", real_week_volume)
        print("month volume is: ", real_month_volume)
        real_time_price = check_real_price(stock_symbol=stock_symbol)
        stock_quote = check_stock_symbol(stock_symbol=stock_symbol)
        # recommendation = get_stock_recommendation(real_time_price, stock_quote)
        recommendation = get_stock_recommendation(real_30min_volume, avg_volume, real_week_volume, real_month_volume, stock_quote)
        return recommendation


    def _arun(self, stock_symbol: str):
        raise NotImplementedError("Does not support async")

    args_schema: Optional[Type[BaseModel]] = InvestingAdvisorCheckInput


# # Warren Buffet
#
# 1. OPERATING MARGIN GREATER THAN OR EQUAL TO INDUSTRY MEDIAN
# 2. PROFIT MARGIN GREATER THAN OR EQUAL TO INDUSTRY MEDIAN
# 3. TOTAL LIABILITIES/TOTAL ASSETS RATIO LESS THAN INDUSTRY MEDIAN
# 4. EPS GROWTH RATE %, 5 YR PCT RANK ≥ 75
# 5. EPS 3-YR GROWTH RATE GREATER THAN OR EQUAL TO 5-YR GROWTH RATE
# 6. EPS, TRAILING 4 QTRS > 0	6.95
# 7. EPS, FISCAL YEAR - LST REPTD YR
# 8. > 0	5.15
# 9. EPS, FISCAL YEAR - 1 YR AGO > 0
# 10. EPS, FISCAL YEAR - 2 YRS AGO > 0
# EPS, FISCAL YEAR - 3 YRS AGO > 0
# EPS, FISCAL YEAR - 4 YRS AGO > 0
# EPS, FISCAL YEAR - 5 YRS AGO > 0
# EPS, FISCAL YEAR - 6 YRS AGO > 0
# RETURN ON EQUITY> 12 %
# ROE, 5-YEAR AVERAGE > 12 %
# SUSTAINABLE GROWTH >= 15 %



