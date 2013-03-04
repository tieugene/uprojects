#include <iostream>
#include <fstream>
#include <cstdlib>
#include <unistd.h>
#include <db_cxx.h>

// compile: gcc -ldb_cxx -o rpm-qa1 rpm-qa1.cpp

// Forward declarations
int show_all_records(Db &);

int main (void)
{
    char *dbname = "/var/lib/rpm/Name";
    Db db(NULL, 0);

    // 1. open db
    try
    {
        // Redirect debugging information to std::cerr
        db.set_error_stream(&std::cerr);

        // Open the database
        db.open(NULL, dbname, NULL, DB_HASH, DB_RDONLY, 0);
    }
    // DbException is not a subclass of std::exception, so we need to catch them both.
    catch(DbException &e)
    {
        std::cerr << "Error opening database: " << dbname << "\n" << e.what() << std::endl;
    }
    catch(std::exception &e)
    {
        std::cerr << "Error opening database: " << dbname << "\n" << e.what() << std::endl;
    }

    // 2. read db
    try
    {
        show_all_records(db);
    } catch(DbException &e) {
        std::cerr << "Error reading databases. " << std::endl;
        return (e.get_errno());
    } catch(std::exception &e) {
        std::cerr << "Error reading databases. " << std::endl << e.what() << std::endl;
        return (-1);
    }

    // Close the db
    try
    {
        db.close(0);
    }
    catch(DbException &e)
    {
            std::cerr << "Error closing database"<< "\n" << e.what() << std::endl;
    }
    catch(std::exception &e)
    {
        std::cerr << "Error closing database" << "\n" << e.what() << std::endl;
    }

    return (0);
}

// Shows all the records in the inventory database.
// For each inventory record shown, the appropriate
// vendor record is also displayed.
int show_all_records(Db &db)
{

    // Get a cursor to the db
    Dbc *cursorp;
    try {
        db.cursor(NULL, &cursorp, 0);

        // Iterate over the database, from the first record to the last, displaying each in turn
        Dbt key, data;
        int ret = cursorp->get(&key, &data, DB_SET);
        if (!ret) {
            do {
                std::cout << key.get_data() << std::endl;
            } while (cursorp->get(&key, &data, DB_NEXT_DUP) == 0);
        } else {
            std::cerr << "No records found " << std::endl;
        }
    } catch(DbException &e) {
        db.err(e.get_errno(), "Error in show_all_records");
        cursorp->close();
        throw e;
    } catch(std::exception &e) {
        cursorp->close();
        throw e;
    }

    cursorp->close();
    return (0);
}
