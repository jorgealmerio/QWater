Prepare QGIS

•	Create a new Qgis project
•	Adjust the project coordinate system for Sirgas 2000, in the meridian range of the area where the network will be designed (for example for Salvador - EPSG: 31984).
•	Create shapes for the types of elements that make up the network (using the same project coordinate system):
o	Points: Nodes, Reservoirs and pumps (if any).
o	From lines: excerpts
•	Save the project 
•	Import the planimetric base to be used 
•	Relate the created shapes to the Epanet information types (Plugins/ Qwater / Settings>) 
o	Junctions = Nodes
o	Pipes = Segments
o	Reservoirs = Reservoirs
o	At this stage take the opportunity to input the initial and final population for the network to be analysed.
o	Under the "Pipes" tab insert the relevant pipe properties for the respective pipe diameters and materials
o	In the "Calculations Options" tab, set the maximum allowed velocity (default = 5 m/s)
o	Click the "Select" button and choose the "template_d-w_lps.inp" calculation configuration Click Plugins / Qwater / Make model and accept all messages 
•	For all shapes, save and exit edit mode 
•	Click in <Project / Sticky Options> and click on the horseshoe icon.

Mapping the Network
Reservoir
•	Select the shape of reservoirs and click on the edit button 
•	Enable the layer label to display the "DC_ID" field 
•	Locate all reservoirs (fixed level) by filling the "HEAD" field with the Terrain Dimension. Open the table to verify that all shells have quota.
•	Change the display of the label to ==> 'Node:' || "DC_ID" || '\ n Quotation =' || "HEAD"
•	Save the shape and exit edit mode
Nodes
•	Select the node shape and click the edit button
•	Enable the layer label to display the "DC_ID" field
•	Locate all nodes 
•	Fill in the "ELEVATION" field with the Terrain Quota. Open the table to verify that all nodes have quota. 
•	Change the display of the label to ==> 'Node:' || "DC_ID" || '\ n Quotation =' || "ELEVATION" 
•	Save the shape and exit edit mode


Segments
•	Select the segments shapes and click on the edit button
•	Enable the layer label to display the "DC_ID" field 
•	Trace all segments according to the direction of the predicted flow (from upstream to downstream). A snippet consists of a polyline that starts at the upstream node and ends at the downstream node. Note: Right click to finish. Esc key to cancel the current edit. 
•	Calculate the length of network segments
o	Click on the calculator button (abacus).
o	Click on "Update an existing field" and select the "LENGTH" field.
o	In "Geometry" select the "$ length" function and click OK. Open the table to verify that you have filled in the "LENGTH" field with the length of each excerpt in meters.
o	Click the OK button. 
•	Assign a preliminary diameter to the passages.
o	Click on the calculator button (abacus). 
o	Click on "Update an existing field" and select the "DIAMETER" field. 
o	In the edit area of the calculator enter 100 (internal diameter 100 mm). 
o	Click the OK button. Check that you have filled in each section the "DIAMETER" field with the provisional value (equal to 100 mm). 
•	Complete roughness information, point loss coefficient and status of the sections. 
o	Update the "ROUGHNESS" field (roughness of the tube, depending on the material, for example 0.1 mm) with the calculator. 
o	Update the "MINORLOSS" field (if not consider adopting equal to 0) with the calculator 
o	Update the field "STATUS" (tube open = 'OPEN' or closed = 'CLOSE') with the calculator. 
•	Save the shape and exit edit mode.
Calculating Demand
•	Click <Plugins / Qwater / Calc Flow>. The message "Demand on nodes calculated successfully" should appear. This routine calculates the unit flow from the distributed demand by allocating at each node the product of the unit flow times half the length of the segments connected to the node. 
•	Save the node shape and exit edit mode.
Preliminary Network Simulation
•	Click <Plugins / Qwater / Run Epanet Simulation> and wait for the message to be displayed. If the message indicates the occurrence of errors, analyze the error feedback in the "Report" tab. 
•	If the simulation was successful, save the shapes and exit the edit mode.
Optimisation of the Network Diameters
•	Click <Plugins / Qwater / Calculate economics diameter> and confirm the message to replace the values in the "DIAMETER" field.
•	Save shapes and exit edit mode. 
Network simulation with optimized diameters 
•	Click <Plugins / Qwater / Run Epanet Simulation> and wait for the message to be displayed. 
•	If the simulation was successful, save the shapes and exit the edit mode.


Final Adjustments
•	Save the project
•	Save the project (suggestion previous name plus result, eg: Network_result.qgs).
•	Click <Plugins / Qwater / Load default Styles>.
•	Analyze the results and fine-tune the reservoir height, diameters of segments.
•	Rosolve the network again (<Plugins / Qwater / Run Epanet Simulation>) 
•	Save the shapes and exit edit mode. 
•	Save the project. 
•	Export the network designed for the dxf format. Adopt a compatible scale.
