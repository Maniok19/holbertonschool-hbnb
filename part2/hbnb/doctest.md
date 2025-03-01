# Cas de Test  

## Création de Ressources (Cas Réussis)  
Ces tests vérifient que les entités sont bien créées lorsque des données valides sont fournies :  

- **Création d’un user** (`test_create_user`)  
- **Création d’une place** (`test_create_place`)  
- **Création d’une amenity** (`test_create_amenity`)  
- **Création d’un review** (`test_create_review`)  

Chaque test envoie une requête **POST** et s’assure que la réponse renvoyée est **201**.  

## Création avec Données Invalides (Cas Limites)  
Des tests ont été menés pour vérifier la gestion des erreurs lorsque des données incorrectes sont envoyées :  

- **User avec des champs manquants** (`test_create_user_invalid_data`)  
- **Place avec des champs mal orthographiés** (`test_create_place_invalid_data`)  
- **Amenity avec un corps de requête vide** (`test_create_amenity_invalid_data`)  
- **Review avec des champs invalides** (`test_create_review_invalid_data`)  

Le serveur doit renvoyer une erreur **400**, indiquant un problème de validation.  

## Récupération des Ressources (Cas Réussis)  
Ces tests s’assurent que l’API permet de récupérer correctement les ressources existantes :  

- **Récupération de tous les users, places, amenities et reviews**  
  (`test_get_users`, `test_get_places`, `test_get_amenities`, `test_get_reviews`)  
- **Récupération par ID**  
  (`test_get_user_by_id`, `test_get_place_by_id`, `test_get_amenity_by_id`, `test_get_review_by_id`)  

Le code de réponse attendu est **200**.  

## Récupération avec ID Invalide (Cas Limites)  
L’objectif de ces tests est de vérifier que l’API renvoie bien une erreur **404** lorsque l’ID fourni est incorrect :  

- **User inexistant** (`test_get_user_by_id_invalid_data`)  
- **Place inexistant** (`test_get_place_by_id_invalid_data`)  
- **amenity inexistante** (`test_get_amenity_by_id_invalid_data`)  
- **Review inexistant** (`test_get_review_by_id_invalid_data`)  

## Mise à Jour des Ressources (Cas Réussis)  
Ces tests valident la mise à jour des ressources avec des données valides :  

- **Mise à jour d’un user** (`test_update_user`)  
- **Mise à jour d’un place** (`test_update_place`)  
- **Mise à jour d’une amenity** (`test_update_amenity`)  
- **Mise à jour d’un review** (`test_update_review`)  

Le code de réponse attendu est **200**.  

## Mise à Jour avec Données Invalides (Cas Limites)  
Des tests ont été effectués pour s’assurer que l’API retourne une erreur **400** lorsque des données incorrectes sont soumises :  

- **Mise à jour d’un user avec un champ inconnu** (`test_update_user_invalid_data`)  
- **Mise à jour d’une place avec des champs incorrects** (`test_update_place_invalid_data`)  

# Conclusion  
Ces tests garantissent la robustesse de l’API en couvrant aussi bien les cas d’usage classiques que les scénarios d’erreur. La gestion des erreurs est bien prise en charge, avec des réponses adaptées en fonction des situations rencontrées.  
