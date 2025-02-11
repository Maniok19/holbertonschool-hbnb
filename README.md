## AirBnB Clone Project

A comprehensive web application that replicates the core functionalities of AirBnB. This project demonstrates a full-stack implementation using a layered architecture approach.
This document presents the project to develop a housing location platform inspired by the Airbnb site. The goal is to design an application that allows users to publish, search and book accommodation intuitively and securely.
# Files
- [ClassDiagram.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/ClassDiagram.mmd "ClassDiagram.mmd")
- [PackageDiagram.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/PackageDiagram.mmd "PackageDiagram.mmd")
- 
- [README.md](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/README.md "README.md")
- [SequenceDiagramUserRegistration.mmd](https://github.com/Maniok19/holbertonschool-hbnb/blob/main/SequenceDiagramUserRegistration.mmd "SequenceDiagramUserRegistration.mmd")

## AirBnB Clone Project

A comprehensive web application that replicates the core functionalities of AirBnB. This project demonstrates a full-stack implementation using a layered architecture approach.

### Architecture Overview

The application follows a three-tier architecture:
```mermaid
classDiagram

class PresentationLayer {
    +UserController
    +PlaceController
    +ReviewController
    +AmenityController
    +WebServices
    +ClientUI
}

class BusinessLogicLayer {
    +UserManager
    +PlaceManager
    +ReviewManager
    +AmenityManager
}

class PersistenceLayer {
    +UserDAO
    +PlaceDAO
    +ReviewDAO
    +AmenityDAO
    +DatabaseConnection
}

PresentationLayer --> BusinessLogicLayer : Facade Pattern (Service Interface)
BusinessLogicLayer --> PersistenceLayer : Data Access Operations
```


### Data Model

The application's data structure is represented in the following class diagram:
```mermaid
classDiagram
  class Super{
    + UUID id
    + DateTime createdAt
    + DateTime updatedAt
  }
  class User {

    + string firstName
    + string lastName
    + string email
    + string password
    + boolean isAdmin
    + register()
    + updateProfile()
    + delete()
    + update to admin()
  }
  class Place {
    + string title
    + string description
    + float price
    + float latitude
    + float longitude
    + UUID ownerId
    + create()
    + update()
    + delete()
    + list()
  }
  class Review {

    + UUID placeId
    + UUID userId
    + int rating
    + string comment
    + create()
    + update()
    + delete()
    + listByPlace()
  }
  class Amenity {

    + string name
    + string description
    + create()
    + update()
    + delete()
    + list()
  }

  Super ..|> User
  Super ..|> Place
  Super ..|> Review
  Super ..|> Amenity
  User "1" o-- "0..*" Place : owns
  Place "1" o-- "0..*" Review : has
  Place "0..*" o-- "0..*" Amenity : has
  User "1" o-- "0..*" Review : has
```
### Technologies Used
To be completed

### Installation
To be completed

### Core Functionalities
#### User Registration Flow
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (e.g., Register User)
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API-->>User: Return Success/Failure
```

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

# Authors
Esteban Cratere
Mano Delcourt 
Herve Le Guennec