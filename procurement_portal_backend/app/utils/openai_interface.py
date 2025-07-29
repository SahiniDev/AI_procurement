import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_commodity_prompt(offer_document: str):
    """
    Generates a prompt for OpenAI API to assign commodity groups to items in the offer document.

    Args:
        offer_document (str): The entire offer document containing all information.

    Returns:
        str: The generated prompt.
    """
    commodity_groups = """
    #### Commodity Groups

    | ID  | Category                | Commodity Group                  |
    |-----|-------------------------|-----------------------------------|
    | 001 | General Services        | Accommodation Rentals            |
    | 002 | General Services        | Membership Fees                  |
    | 003 | General Services        | Workplace Safety                 |
    | 004 | General Services        | Consulting                       |
    | 005 | General Services        | Financial Services               |
    | 006 | General Services        | Fleet Management                 |
    | 007 | General Services        | Recruitment Services             |
    | 008 | General Services        | Professional Development         |
    | 009 | General Services        | Miscellaneous Services           |
    | 010 | General Services        | Insurance                        |
    | 011 | Facility Management     | Electrical Engineering           |
    | 012 | Facility Management     | Facility Management Services     |
    | 013 | Facility Management     | Security                         |
    | 014 | Facility Management     | Renovations                      |
    | 015 | Facility Management     | Office Equipment                 |
    | 016 | Facility Management     | Energy Management                |
    | 017 | Facility Management     | Maintenance                      |
    | 018 | Facility Management     | Cafeteria and Kitchenettes       |
    | 019 | Facility Management     | Cleaning                         |
    | 020 | Publishing Production   | Audio and Visual Production      |
    | 021 | Publishing Production   | Books/Videos/CDs                 |
    | 022 | Publishing Production   | Printing Costs                   |
    | 023 | Publishing Production   | Software Development for Publishing |
    | 024 | Publishing Production   | Material Costs                   |
    | 025 | Publishing Production   | Shipping for Production          |
    | 026 | Publishing Production   | Digital Product Development      |
    | 027 | Publishing Production   | Pre-production                   |
    | 028 | Publishing Production   | Post-production Costs            |
    | 029 | Information Technology  | Hardware                         |
    | 030 | Information Technology  | IT Services                      |
    | 031 | Information Technology  | Software                         |
    | 032 | Logistics               | Courier, Express, and Postal Services |
    | 033 | Logistics               | Warehousing and Material Handling |
    | 034 | Logistics               | Transportation Logistics         |
    | 035 | Logistics               | Delivery Services                |
    | 036 | Marketing & Advertising | Advertising                      |
    | 037 | Marketing & Advertising | Outdoor Advertising              |
    | 038 | Marketing & Advertising | Marketing Agencies               |
    | 039 | Marketing & Advertising | Direct Mail                      |
    | 040 | Marketing & Advertising | Customer Communication           |
    | 041 | Marketing & Advertising | Online Marketing                 |
    | 042 | Marketing & Advertising | Events                           |
    | 043 | Marketing & Advertising | Promotional Materials            |
    | 044 | Production              | Warehouse and Operational Equipment |
    | 045 | Production              | Production Machinery             |
    | 046 | Production              | Spare Parts                      |
    | 047 | Production              | Internal Transportation          |
    | 048 | Production              | Production Materials             |
    | 049 | Production              | Consumables                      |
    | 050 | Production              | Maintenance and Repairs          |
    """

    prompt = f"""
    Assign each item in the following offer document to one or more of the commodity groups listed below:

    {commodity_groups}

    Offer Document:
    {offer_document}

    Please provide the information below if available and give answer in JSON format,
    If something is not available, use "N/A" as the value:
    ```

    - Vendor Name: [Vendor Name]
    - Umsatzsteuer-Identifikationsnummer (VAT ID): [VAT ID]
    - Requestor Department: [Requestor Department]
    - Order Lines:
      - Item 1:
        - Product: [Product Name]
        - Unit Price: [Unit Price]
        - Quantity: [Quantity]
        - Total: [Total Price]
        - Commodity Groups: [Commodity Group]
      - Item 2:
        - Product: [Product Name]
        - Unit Price: [Unit Price]
        - Quantity: [Quantity]
        - Total: [Total Price]
        - Commodity Groups: [Commodity Group]
    - Total Cost: [Total Cost]

    ```
    """

    return prompt
