# holbertonschool-hbnb

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