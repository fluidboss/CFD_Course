    Info<< "Reading transportProperties\n" << endl;

    IOdictionary transportProperties
    (
        IOobject
        (
            "transportProperties",
            runTime.constant(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        )
    );
//dimensionedScalar("dim_s", dimTime, mesh.lookupObject<IOdictionary>("transportProperties"));
dimensionedScalar dim_s("dim_s",dimensionSet(0,0,1,0,0,0,0),readScalar(transportProperties.lookup("dim_s")));
dimensionedScalar dim_m("dim_m",dimensionSet(0,1,0,0,0,0,0),readScalar(transportProperties.lookup("dim_m")));
dimensionedScalar g("g",dimensionSet(0,1,-2,0,0,0,0),readScalar(transportProperties.lookup("g")));
dimensionedScalar Hdry("Hdry",dimensionSet(0,1,0,0,0,0,0), readScalar(transportProperties.lookup("Hdry")));
dimensionedScalar Hdry2("Hdry2",dimensionSet(0,1,0,0,0,0,0),readScalar(transportProperties.lookup("Hdry2")));
dimensionedScalar Cnu("Cnu",dimensionSet(0,0,0,0,0,0,0),readScalar(transportProperties.lookup("Cnu")));
dimensionedScalar nutmax("nutmax",dimensionSet(0,2,-1,0,0,0,0),readScalar(transportProperties.lookup("nutmax")));
dimensionedScalar rhoInf("rhoInf",dimensionSet(1,-3,0,0,0,0,0),1000);


//    Info<< "Reading field H\n" << endl;
//    Info<< "Flow depth\n" << endl;

    volScalarField H
    (
        IOobject
        (
            "H",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        mesh
    );

//      Info<< "Reading field Hclip\n" << endl;
//    Info<< "Flow depth\n" << endl;
//  Info<< "Hdry\n" << Hdry << endl;
    
    volScalarField Hclip
    (
        IOobject
        (
            "Hclip",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::NO_WRITE
        ),
(H-Hdry)*pos(H-Hdry) + Hdry        
    );

    Info<< "Reading field S\n" << endl;
    Info<< "Bottom elevation\n" << endl;
    volScalarField S
    (
        IOobject
        (
            "S",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        mesh
    );
  //  Info<< "Reading field kst\n" << endl;
   // Info<< "Strickler value\n" << endl;
    volScalarField kst
    (
        IOobject
        (
            "kst",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        mesh
    );

  // Info<< "Reading field HU\n" << endl;
    volVectorField HU
    (
        IOobject
        (
            "HU",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        mesh
    );

    volScalarField rho
    (
        IOobject
        (
            "rho",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::NO_WRITE
        ),
        mesh
    );

    //Info<< "Creating field U\n" << endl;
    volVectorField U
    (
        IOobject
        (
            "U",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        HU/dim_m
    );

   volScalarField Fr
    (
        IOobject
        (
            "Fr",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        mag(HU)/(Foam::pow(g,0.5)*Foam::pow(H,1.5))
    );

   volVectorField tau_b
    (
        IOobject
        (
            "tau_b",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        U*mag(U)
    );

    Info<< "Creating field P\n" << endl;
    volScalarField p
    (
        IOobject
        (
            "p",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        0.5*H*H*g*rhoInf/(dim_m)
    );

    Info<< "Creating field phi\n" << endl;
    surfaceScalarField phi
    (
        IOobject
        (
            "phi",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        linearInterpolate(U) & mesh.Sf()
    );

    Info<< "Creating field alpha\n" << endl;
    volScalarField alpha
    (
        IOobject
        (
            "alpha",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        (g*dim_s*dim_s/dim_m)*mag(U)/pow(kst,2.0)/pow(Hclip/dim_m,1.0/3.0)/Hclip
    );


   Info<< "Creating field nut\n" << endl;
    volScalarField nut
    (
        IOobject
        (
            "nut",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        mesh
	);


   Info<< "Creating field wetDry\n" << endl;
    volScalarField wetDry
    (
        IOobject
        (
            "wetDry",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        pos(H-Hdry)
	);

   volScalarField divU
    (
        IOobject
        (
            "divU",
            runTime.timeName(),
            mesh,
            IOobject::READ_IF_PRESENT,
            IOobject::AUTO_WRITE
        ),
        fvc::div(U)
	);

   volVectorField curltaub
    (
        IOobject
        (
            "divtaub",
            runTime.timeName(),
            mesh,
            IOobject::MUST_READ,
            IOobject::AUTO_WRITE
        ),
        fvc::curl(tau_b)
	);

    Info<< "createFields done\n" << endl;


    Info<< "createFields done\n" << endl;
