import asyncpg
import asyncio
from typing import Dict, Any, List

async def get_conn():
    return await asyncpg.connect(
         host="localhost",
        port="5432",
        database="DispatcherIQ",
        user="postgres",
        password="counterstrike1.6mylife"
    )

async def insert_records(tableName:str , row: Dict[str, Any]) -> None:
    
    conn = await get_conn()
    # Get table columns from Postgres information schema
    
    query_columns = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = $1
        ORDER BY ordinal_position;
    """

    table_columns: List[str] = [r["column_name"] for r in await conn.fetch(query_columns, tableName)]
    
    if not table_columns:
        raise ValueError(f"Table '{tableName}' does not exist or has no columns.")
    
    
    input_columns = list(row.keys()) # Extract keys from the given row
    
    
    for col in input_columns:        # Check if all input keys exist in table columns
        if col not in table_columns:
            raise ValueError(f"Column '{col}' does not exist in table '{tableName}'.")
    
    
    # Optional: Check missing columns (only if required — skip if defaults exist)
    # missing = set(table_columns) - set(input_columns)
    # print("Missing columns that have defaults:", missing)
    # Build SQL dynamically
    columns_str = ", ".join(input_columns)
    placeholders = ", ".join(f"${i+1}" for i in range(len(input_columns)))
    values = list(row.values())
    insert_sql = f"INSERT INTO {tableName} ({columns_str}) VALUES ({placeholders})"
    
    print(columns_str)
    print(placeholders)
    print(values)
    print(insert_sql)

    # Execute
    await conn.execute(insert_sql, *values)
    print(f"Inserted 1 row into {tableName}")


employee_record = {
    "name": "Mohit",
    "role": "Data Engineer",
    "salary": 2467
}
asyncio.run(insert_records('employees',employee_record))