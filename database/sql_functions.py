import json
import logging
from typing import Dict, Any
from pymysql import connect, Error as MySQLError
from contextlib import contextmanager

##########################################	GLOBAL SCOPE	#######################################
# logs
logger = logging.getLogger(__name__)

##########################################	FUNCTIONS	###########################################

@contextmanager
def create_connection(db_config):
    conn = None
    try:
        conn = connect(**db_config)
        logging.info("Successfull database connection.")
        yield conn
    except MySQLError as err:
        logging.error(f"MySQL error when connecting to database: {err.args[1]}")
        raise 
    finally:
        if conn :
            conn.close()
            logging.info("Database connection closed.")

#--------------------------------------------------------------------------------------------------

def is_record_exist(cursor, table_name: str, record_data: Dict[str, Any]) -> bool:
    """
    Check if a record exists in the specified table.

    Args:
        cursor: A MySQL cursor object.
        table_name (str): The name of the table to check.
        record_data (Dict[str, Any]): A dictionary of column names and values to check for existence.

    Returns:
        bool: True if the record exists, False otherwise.

    Raises:
        Error: If a MySQL-specific error occurs.
        Exception: For any other unexpected errors.
    """
    try :
        placeholders = " AND ".join(f"(`{col}` IS NULL OR `{col}` = %s)" for col in record_data.keys())
        sql = f"SELECT EXISTS(SELECT 1 FROM `{table_name}` WHERE {placeholders} ) AS is_exist"
        
        values = tuple(record_data.values())

        # Print the full SQL query with arguments
        # full_query = cursor.mogrify(sql, values)
        # logger.debug(f"Full SQL query: {full_query}")

        cursor.execute(sql, values)

        result = cursor.fetchone() # Get request result
        return bool(result['is_exist']) if result else False
    
    except MySQLError as err:
        logger.error(f"MySQL error when checking record existence: {err.args[1]}")
        logger.error(f"Table: {table_name}, Data: \n{json.dumps(record_data, indent = 4)}")
        raise
    except Exception as e :
        logger.error(f"An unexpected error has occurred: {e}")
        raise

#--------------------------------------------------------------------------------------------------

def insert(conn: connect, table_name: str, records_data: list[Dict[str, Any]], batch_size : int = 1000):
    """
    Insert records into the specified table using batch processing.

    Args:
        conn (connect): MySQL connection object.
        table_name (str): Name of the table to insert into.
        records_data (List[Dict[str, Any]]): List of records to insert.
        batch_size (int): Number of records to insert in each batch. Defaults to 1000.

    Returns:
        int: Number of records successfully inserted.

    Raises:
        ValueError: If records_data is empty.
        Error: If a MySQL-specific error occurs.
        Exception: For any other unexpected errors.

    Notes:
        Use batch processing to :
        - Reduce the load on memory
        - Minimize the duration of each transaction
        - Facilitate error recovery
    """
    if records_data == [] :
            raise ValueError(f"Records data for {table_name} is empty.")
    
    inserted_count = 0
    try :
        with conn.cursor() as cursor:
            for i in range(0, len(records_data), batch_size) :
                # Use batch processing 
                batch_data = records_data[i:i+batch_size]

                for record in batch_data :
                    if not is_record_exist(cursor, table_name, record) :
                        columns = ", ".join(f"`{col}`" for col in record.keys())
                        placeholders = ", ".join(["%s"] * len(record))
                        sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"

                        values = tuple(record.values())
                        cursor.execute(sql, values)
                        inserted_count += 1
                    # else:
                    #     logger.warning(f"Record already exists: {json.dumps(record, indent = 4)}")
                    
                conn.commit()

        logger.info(f"Inserted {inserted_count}/{len(records_data)} records into {table_name}")
    except MySQLError as err:
        logger.error(f"MySQL error when insert record : {err.args[1]}")
        logger.error(f"Table: {table_name}, Data: \n{json.dumps(record, indent = 4)}")
        conn.rollback()
        raise
    except ValueError as val_err:
        logger.error(f"{val_err}")
        conn.rollback()
        raise
    except Exception as e :
        logger.error(f"An unexpected error has occurred: {e}")
        conn.rollback()
        raise

#--------------------------------------------------------------------------------------------------

def insert_or_ignore(conn: connect, table_name: str, records_data: list[Dict[str, Any]], batch_size : int = 1000):
    """
        Use batch processing to :
        - Reduce the load on memory
        - Minimize the duration of each transaction
        - Facilitate error recovery

    Args:
        conn (connect): _description_
        table_name (str): _description_
        records_data (list[Dict[str, Any]]): _description_
    """
    if records_data == [] :
            raise ValueError(f"Records data for {table_name} is empty.")
    
    inserted_count = 0
    try :
        with conn.cursor() as cursor:
            for i in range(0, len(records_data), batch_size) :
                # Use batch processing 
                batch_data = records_data[i:i+batch_size]

                for record in batch_data :
                    columns = ", ".join(f"`{col}`" for col in record.keys())
                    placeholders = ", ".join(["%s"] * len(record))
                    sql = f"INSERT IGNORE INTO `{table_name}` ({columns}) VALUES ({placeholders})"

                    values = tuple(record.values())
                    cursor.execute(sql, values)
                    inserted_count += 1

                conn.commit()

        logger.info(f"Inserted {inserted_count}/{len(records_data)} records into {table_name}")
    except MySQLError as err:
        logger.error(f"MySQL error when insert record : {err.args[1]}")
        logger.error(f"Table: {table_name}, Data: \n{json.dumps(record, indent = 4)}")
        conn.rollback()
        raise
    except ValueError as val_err:
        logger.error(f"{val_err}")
        conn.rollback()
        raise
    except Exception as e :
        logger.error(f"An unexpected error has occurred: {e}")
        conn.rollback()
        raise

#--------------------------------------------------------------------------------------------------

def insert_with_update(conn: connect, table_name: str, records_data: list[Dict[str, Any]], batch_size : int = 1000):
    """
        Use batch processing to :
        - Reduce the load on memory
        - Minimize the duration of each transaction
        - Facilitate error recovery

    Args:
        conn (connect): _description_
        table_name (str): _description_
        records_data (list[Dict[str, Any]]): _description_
    """
    if records_data == [] :
            raise ValueError(f"Records data for {table_name} is empty.")
    
    inserted_count = 0
    try :
        with conn.cursor() as cursor:
            for i in range(0, len(records_data), batch_size) :
                # Use batch processing 
                batch_data = records_data[i:i+batch_size]

                for record in batch_data :
                    columns = ", ".join(f"`{col}`" for col in record.keys())
                    placeholders = ", ".join(["%s"] * len(record))
                    update_str = ", ".join([f"{col} = VALUES({col})" for col in record.keys()])
                    sql = f"""
                            INSERT INTO `{table_name}` ({columns}) 
                            VALUES ({placeholders})
                            ON DUPLICATE KEY UPDATE {update_str}
                        """
                    
                    values = tuple(record.values())
                    cursor.execute(sql, values)
                    inserted_count += 1

                conn.commit()
        logger.info(f"Inserted {inserted_count}/{len(records_data)} records into {table_name}")
    except MySQLError as err:
        logger.error(f"MySQL error when insert record : {err.args[1]}")
        logger.error(f"Table: {table_name}, Data: \n{json.dumps(record, indent = 4)}")
        conn.rollback()
        raise
    except ValueError as val_err:
        logger.error(f"{val_err}")
        conn.rollback()
        raise
    except Exception as e :
        logger.error(f"An unexpected error has occurred: {e}")
        conn.rollback()
        raise