# The purpose
<p>This is a tutorial that demonstrates the use of neomodel and python to create and query data in/from neo4j. The technologies used are: </p>
<ul>
    <li>neo4j</li>
    <li>Python</li>
    <li>neomodel</li>
</ul>

<p>Though not required, it will be helpful if you would have gone through neomodel documentation at: 
<h>https://neomodel.readthedocs.io/en/latest/</h> </p>

# Pre-requisites
<p>Install Neo4J and run it with default configurations (bolt://localhost:7687). Change the password to "password"</p>
<p>Install Python. Install <u>neomodel</u> using command <u>pip install neomodel</u></p>

# Run it
<p>After cloning the repo, go to your project directory, and run the following command from command line: <u>
neomodel_install_labels --db bolt://neo4j:password@localhost:7687 model.py</u> This will create required schema and 
constraints in neo4j.</p> 
<p>Then run the command: <u>python app.py</u>. This should execute various queries and print the results.</p>