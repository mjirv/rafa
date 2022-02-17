## Rafa Sample Project

### Quickstart
1. Run `pip3 install rafa`
2. In this directory, run `python3 project.py`
3. Use your favorite SQLite client to connect to the demo DB and see the tables created.
    - The project prints the location of the database when you run it
    - For example:
        ```michael@DESKTOP-URS6SAQ:~/rafa/sample_project$ python3 project.py 
            Indexing schema. This will take a second...finished!
            /home/michael/.local/lib/python3.8/site-packages/db/data/chinook.sqlite
        ```
    - Using the command line, you could do:
        ```
            $ sqlite3
            $   sqlite > .open /home/michael/.local/lib/python3.8/site-packages/db/data/chinook.sqlite
            $   sqlite > select * from invoices limit 10;
        ```