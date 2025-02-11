## AirBnB Clone Project

A comprehensive web application that replicates the core functionalities of AirBnB. This project demonstrates a full-stack implementation using a layered architecture approach.
This document presents the project to develop a housing location platform inspired by the Airbnb site. The goal is to design an application that allows users to publish, search and book accommodation intuitively and securely.
# Files
- [ClassDiagram.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/ClassDiagram.mmd "ClassDiagram.mmd")
- [PackageDiagram.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/PackageDiagram.mmd "PackageDiagram.mmd")
- 
- [README.md](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/README.md "README.md")
- [SequenceDiagramUserRegistration.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/SequenceDiagramUserRegistration.mmd "SequenceDiagramUserRegistration.mmd")

### Architecture Overview

The application follows a three-tier architecture:
```mermaid
classDiagram# holbertonschool-hbnb

## AirBnB Clone Project

A comprehensive web application that replicates the core functionalities of AirBnB. This project demonstrates a full-stack implementation using a layered architecture approach.

### Architecture Overview

The application follows a three-tier architecture:
```mermaid
classDiagram
  class PresentationLayer {
    <<Interface>>
    + ServiceAPI
  }
  class BusinessLogicLayer {
    + ModelClasses
  }
  class PersistenceLayer {
    + DatabaseAccess
  }
  PresentationLayer -- BusinessLogicLayer : Facade Pattern
  BusinessLogicLayer -- PersistenceLayer : Database Operations
```
### Core Functionalities

#### User Registration Flow
![User Registration](SequenceDiagramUserRegistration.mmd)

#### Place Management
- **Place Creation:**
![Place Creation](SequenceDiagramPlaceCreation.mmd)

- **Place Listing:**
![Fetch Places](SequenceDiagramFetchPlaces.mmd)

- **Review Submission:**
![Review Submission](SequenceDiagramReviewSubmission.mmd)

### Data Model

The application's data structure is represented in the following class diagram:

![Class Diagram](ClassDiagram.mmd)

### Technologies Used
To be completed

### Installation
To be completed
  class PresentationLayer {
    <<Interface>>
    + ServiceAPI
  }
  class BusinessLogicLayer {
    + ModelClasses
  }
  class PersistenceLayer {
    + DatabaseAccess
  }
  PresentationLayer -- BusinessLogicLayer : Facade Pattern
  BusinessLogicLayer -- PersistenceLayer : Database Operations
```
### Core Functionalities

#### User Registration Flow
![User Registration](SequenceDiagramUserRegistration.mmd)

#### Place Management
- **Place Creation:**
![Place Creation](SequenceDiagramPlaceCreation.mmd)

- **Place Listing:**
![Fetch Places](SequenceDiagramFetchPlaces.mmd)

- **Review Submission:**
![Review Submission](SequenceDiagramReviewSubmission.mmd)

### Data Model

The application's data structure is represented in the following class diagram:

![Class Diagram](ClassDiagram.mmd)

### Technologies Used
To be completed

### Installation
To be completed
To be completed
# Authors
Esteban Cratere
Mano Delacourt 
Herve Le Guennec