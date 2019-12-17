CREATE TABLE recipe (
       id INT PRIMARY KEY,
       title VARCHAR(120) NOT NULL,
       instructions VARCHAR(4096),
       total_energy FLOAT,
       energy_per_serving FLOAT,
       protein FLOAT,
       fat FLOAT,
       carbohydrates FLOAT);

CREATE TABLE ingredients (
       recipe_id INT,
       amount FLOAT DEFAULT 0.0,
       unit VARCHAR(10),
       name VARCHAR(128),
       CONSTRAINT ingredient_recipe
       FOREIGN KEY (recipe_id)
               REFERENCES recipe(id)
       ); 
      
