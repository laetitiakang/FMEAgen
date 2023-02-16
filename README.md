# FMEAgen

In the context of product design, it is important to be able to assess the risks associated with product malfunction. 
These risks are formalized in the form of failure modes. Risk management aims to identify the causes, probability of occurrence, 
and severity of these modes in order to allow the designer to modify the design to limit or eliminate them. 
Most current risk management methods have a major drawback: they are subjective. 
Therefore, we will seek to eliminate this subjectivity by evaluating all possible risks by a systematic and automated method. 
This will be done by combining the AMDEC and FBS Linkage methods to create a new method that meets these criteria. 

Group 1 : FBS Linkage & failure propagation mode (AnyLogic, Javascript)

1) See folder named : FMECAGen_PropagationV3
2) Open AnyLogic file named : EITM_FBSRiskSimulation_Propagation.alp
3) Run it

Group 2 : FMEA table generator (Python)

1) See folder named : FMECAGen_Python 
2) Open Python file named : ImportFile_20220512
3) Change path of the imported file (FBSdatabase - Copie) if necessary
4) Run ImportFile_20220512


Comments :
If you need more information about the project, read the project report "PJT2A_Rapport_FMEAgen.pdf". The work is not finished yet. Indeed, one part of the code is made with Python, the other with AnyLogic. The goal is to combine the 2 codes, so you have to pass either everything in python or everything in AnyLogic. Enjoy!

