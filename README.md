<h2 style="color: #fff; text-shadow: 1px 1px 0px #5f0370, 1px 1px 0px #9809b1, 2px 2px 0px #d900ff">BestCheerPoms :hibiscus: </h2>

This is a project for private business company Pompoms. 
In this project, I'm responsible for backend part

### Technical stack

| Frontend    | Backend    |
| ------------| ---------- |
| Angular     | Flask      |
| TypeScript  | Python     |
| SASS        | SQLAlchemy |
| HTML        | Docker     |
|             | PostgreSQL |

 ### Start
**Front-end part**
  - go to fronted folder
  - npm i
  - npm run start

 ``sudo docker-compose -f docker-compose.prod.yml up --build``
 cd Projects/pom-poms/

 create tar:
 docker save -o pompoms02.tar pom_back pom_front

 install in new pc:
 docker load -i pompoms02.tar
 docker-compose -f docker-compose_np.yml up


### Config file
__Path__: frontend/assets/config-property.json

  - "weekends": вихідні дні, починаючи з понеділка, де понеділок це 1, відповідно неділя це 7;
  - "exclusionData": дні, які не враховувати при розрахунку, вигляд дати має відповідати стилю YYYY-MM-DD, якщо це більше одної дати, тоді цей період задаємо через '...ʼ:  "2023-06-21...2023-07-01"