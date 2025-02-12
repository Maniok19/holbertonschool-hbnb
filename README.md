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
participant PresentationLayer 
participant BusinessLogic
participant PersistenceLayer

User->>PresentationLayer : API Call (e.g., Register User)
PresentationLayer ->>BusinessLogic: Validate and Process Request
BusinessLogic-->>BusinessLogic: Validate and Process Request
 alt If validation fails
    BusinessLogic-->>PresentationLayer: Returns validation failure
    PresentationLayer-->>User: Returns validation error message
  else If validation succeeds
    BusinessLogic->>PersistenceLayer: Saves re data to database
    PersistenceLayer->>Audit: Logs review creation to the database
    Audit-->>PersistenceLayer: Acknowledges log creation
    PersistenceLayer-->>BusinessLogic: Returns success/failure
    BusinessLogic-->>PresentationLayer: Returns result to presentation
    PresentationLayer-->>User: Returns success/failure message
  end
```

#### Place Management
- **Place Creation:**
```mermaid
sequenceDiagram
  participant User
  participant PresentationLayer
  participant BusinessLogicLayer
  participant PersistenceLayer

  User->>PresentationLayer: Creates a new place with title, description, price, location, ownerId
  PresentationLayer->>BusinessLogicLayer: Validates data and creates place object

  alt Validation success

  
    BusinessLogicLayer->>PersistenceLayer: Saves place data to database
    BusinessLogicLayer->>AuditLogs: Log the new place creation          
        AuditLogs-->>PersistenceLayer:Returns success
  
    PersistenceLayer-->>BusinessLogicLayer: Returns success

    BusinessLogicLayer-->>PresentationLayer: Returns success message
    PresentationLayer-->>User: Returns success message


  else Validation failure
      AuditLogs-->>PersistenceLayer:Returns failed
          PersistenceLayer-->>BusinessLogicLayer: Returns failed
    BusinessLogicLayer-->>PresentationLayer: Returns validation error
    PresentationLayer-->>User: Returns error message
  end
```

- **Place Listing:**
```mermaid
sequenceDiagram
    participant User
    participant PresentationLayer
    participant BusinessLogicLayer
    participant PersistenceLayer

    User->>PresentationLayer: Requests a list of places based on criteria
    Note over User,PresentationLayer: Filters: location, price, amenities

    PresentationLayer->>BusinessLogicLayer: Processes request and retrieves places
    Note over PresentationLayer,BusinessLogicLayer: Validates input parameters

    BusinessLogicLayer->>PersistenceLayer: Fetches place data from database
    Note over BusinessLogicLayer,PersistenceLayer: Builds query with filters

    PersistenceLayer->>PersistenceLayer: Executes SQL query
    PersistenceLayer-->>PersistenceLayer: Raw database results

    PersistenceLayer->>BusinessLogicLayer: Returns list of places
    Note over PersistenceLayer,BusinessLogicLayer: Converts to Place objects

    BusinessLogicLayer->>PresentationLayer: Returns filtered list
    Note over BusinessLogicLayer,PresentationLayer: Applies business rules

    PresentationLayer->>User: Returns formatted list of places
    Note over PresentationLayer,User: JSON/HTML response
```

- **Review Submission:**
```mermaid
sequenceDiagram
  participant User
  participant PresentationLayer
  participant BusinessLogicLayer
  participant PersistenceLayer
  participant Audit

  User->>PresentationLayer: Submits a review for a place with rating and comment
  PresentationLayer->>BusinessLogicLayer: Send the request for review creation
  BusinessLogicLayer-->>BusinessLogicLayer: Validates data and creates review object
   alt if validation succeeds
    BusinessLogicLayer->>PersistenceLayer: Saves review data to database
    PersistenceLayer->>Audit: Logs review creation to the database
    Audit-->>PersistenceLayer: Acknowledges log creation
    PersistenceLayer-->>BusinessLogicLayer: Returns success/failure
    BusinessLogicLayer-->>PresentationLayer: Returns result to presentation
    PresentationLayer-->>User: Returns success/failure message
    else If validation fails
    BusinessLogicLayer-->>PresentationLayer: Returns validation failure
    PresentationLayer-->>User: Returns validation error message
  end
```


# Authors
Esteban Cratere


Mano Delcourt 


Herve Le Guennec