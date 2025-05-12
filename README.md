# {Tutorial: Simulación del UR5 con MoveIt y Gazebo en ROS}
Este tutorial explica paso a paso cómo instalar y configurar el entorno necesario para simular y controlar el robot UR5 con un gripper Robotiq 85 en ROS. Al finalizar, el lector podrá lanzar correctamente el modelo del UR5 con su gripper en Gazebo, visualizarlo en RViz mediante MoveIt y comprobar el funcionamiento de los controladores. Todo está preparado para luego usar el sistema en tareas más complejas como pick and place o control avanzado.

## 📋 Requisitos Previos
- Uso básico de terminal en Linux.
- Conocimientos elementales de ROS (nodos, launch files, catkin).
- Familiaridad básica con URDF y MoveIt

## 🛠️ Herramientas y software requeridos:
- Ubuntu 20.04
- ROS Noetic
- Gazebo (incluido con ROS Noetic)
- MoveIt
- Python 3

## 📖 Introducción
Este tutorial tiene como objetivo documentar el proceso completo para simular y configurar el robot UR5 con un gripper Robotiq 85 en ROS, utilizando herramientas como Gazebo, RViz y MoveIt. A lo largo de este instructivo, se explicará cómo preparar el entorno de trabajo, cargar los modelos del robot, la mesa y los objetos del entorno, y cómo ajustar los controladores y archivos necesarios para que todo funcione de forma integrada.

El enfoque principal es lograr que el robot UR5 y su gripper funcionen correctamente dentro del simulador, con la capacidad de ser controlados desde MoveIt. Este entorno sirve como base para desarrollos más avanzados, como tareas de manipulación, pruebas de algoritmos o integración con visión artificial.

## 💾 Tutorial: 
✅ Paso 0: Instalar el plugin mimic para Gazebo

Este paso es necesario para que el gripper Robotiq funcione correctamente en Gazebo. (Si ya tienes instalado el plugin, puedes omitir este paso)

Para verificar si ya esta instalado, ejecuta en la terminal: 
```
find /usr/ -name "libroboticsgroup_gazebo_mimic_joint_plugin.so"
```
Si el archivo aparece, puedes continuar con el siguiente paso de la guía.
Si no aparece, sigue uno de los métodos de instalación a continuación.

- Opcion 1: Instalar globalmente en el sistema (recomendado con permisos sudo)
  ```
  cd ~
  git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins.git
  cd roboticsgroup_gazebo_plugins
  mkdir build && cd build
  cmake ..
  make
  sudo make install
  ```
- Opción 2 – Instalar dentro del workspace de ROS
  ```
  cd ~/catkin_ws/src
  git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins.git
  cd roboticsgroup_gazebo_plugins
  mkdir build && cd build
  cmake ..
  make
  sudo make install
  ```
📍 Para asegurar que Gazebo encuentre el plugin

A veces Gazebo no encuentra plugins instalados fuera de las rutas estándar. Para evitar errores, agrega lo siguiente a tu ~/.bashrc:
  ```
  echo 'export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:/usr/local/lib' >> ~/.bashrc
  source ~/.bashrc
  ```

✅ Paso 1 – Crear tu workspace catkin_ws

Primero, crea tu espacio de trabajo en ROS y compílalo:
  ```
  mkdir -p ~/catkin_ws/src
  cd ~/catkin_ws
  catkin_make
  source devel/setup.bash
  echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
  ```
Importante: Cada vez que abras una nueva terminal, asegúrate de que el workspace esté correctamente cargado (esto se automatiza con el .bashrc).

✅ Paso 2 – Crear el paquete ur5_v1

Dentro del directorio src, crea un paquete con las dependencias necesarias para el UR5 y su entorno:
  ```
  cd ~/catkin_ws/src
  catkin_create_pkg ur5_v1 controller_manager joint_state_controller robot_state_publisher roscpp rospy std_msgs urdf
  ```
 catkin_create_pkg <nombre_paquete> <dependencias>
En este caso, el paquete se llama ur5_v1.
Luego compila nuevamente:
  ```
  cd ~/catkin_ws
  catkin_make
  ```

✅ Paso 3 – Clonar el repositorio del UR5
Instala el paquete universal-robots para cargar el modelo del UR5, y asegúrate de tener las dependencias necesarias:
  ```
  sudo apt-get install ros-noetic-universal-robots
  ```
Después:
  ```
  cd ~/catkin_ws/src
  git clone -b noetic-devel https://github.com/ros-industrial/universal_robot.git
  cd ~/catkin_ws
  rosdep update
  rosdep install --rosdistro noetic --ignore-src --from-paths src
  catkin_make
  ```
El repositorio incluye los modelos URDF, controladores y archivos de MoveIt necesarios para el UR5.

✅ Paso 4 – Probar que aparezca el UR5 en Gazebo, MoveIt y RViz
Usa tres terminales separadas para este proceso:
- Terminal 1 – Lanzar Gazebo con el UR5
  ```
  roslaunch ur_gazebo ur5_bringup.launch
  ```
  Esto lanza el modelo del UR5 dentro del entorno de simulación Gazebo.
- Terminal 2 – Lanzar MoveIt con planificación habilitada
  ```
  roslaunch ur5_moveit_config moveit_planning_execution.launch sim:=true
  ```
  Esto lanza MoveIt y conecta los controladores simulados para la planificación de movimientos.
- Terminal 3 – Lanzar RViz para visualización
  ```
  roslaunch ur5_moveit_config moveit_rviz.launch config:=true
  ```
  Dentro de RViz:
  - En la parte superior izquierda, en "Fixed Frame", selecciona base_link.
  - En la parte inferior izquierda, haz clic en "Add", y selecciona "RobotModel" para visualizar el UR5.

![Imagen prueba](URL_de_la_imagen)


✅ Paso 5 – Crear archivo .xacro con configuración personalizada del UR5
1. Lanzar el Setup Assistant de MoveIt
  ```
  cd ~/catkin_ws
  roslaunch moveit_setup_assistant setup_assistant.launch
  ```
- Haz clic en "Edit Existing MoveIt Configuration Package".
- Introduce esta ruta (ajusta si tu usuario no es gazebo-ros):
```
/home/gazebo-ros/catkin_ws_6/src/universal_robot/ur5_moveit_config
```
- Haz clic en LOAD.
- Ve a la pestaña "Simulation" y copia todo el contenido de texto.
- Cierra el MoveIt Setup Assistant.


2. Crear carpeta urdf y archivo .xacro
```
cd ~/catkin_ws/src/ur5_v1
mkdir urdf
cd urdf
touch ur5_1.xacro
```
Abre el archivo con tu editor favorito (VSCode) y pega el contenido copiado del paso anterior.


3. Correcciones necesarias al .xacro
Cambia todas las apariciones de:
```
<type>PositionJointInterface</type>
```
por:
```
<type>EffortJointInterface</type>
```
Abajo de esta sección:
```
<link name="base_link" />
<link name="base_link_inertia">
...
</link>
```
Agrega el siguiente bloque para fijar el robot al mundo:
```
<!-- Fix the cobot to the world -->
<link name="world"/>

<joint name="fixed" type="fixed">
    <parent link="world"/>
    <child link="base_link"/>   
</joint>
```

✅ Paso 6 – Crear archivo launch para mostrar el robot en RViz
1. Crear carpeta launch dentro de tu paquete
```
cd ~/catkin_ws/src/ur5_v1
mkdir launch
cd launch
touch rviz_ur5.launch
```
2. Contenido del archivo rviz_ur5.launch
   Asegúrate de que el nombre del paquete (ur5_v1) y el archivo .xacro (ur5_1.xacro en este ejemplo) coincidan con los nombres que realmente estás usando.
    ```
    <?xml version="1.0"?>
    <launch>
    
        <!-- Cargar el modelo URDF convertido desde xacro -->
        <param name="robot_description" command = "$(find xacro)/xacro --inorder $(find ur5_v1)/urdf/ur5_4.xacro" />
    
        <!-- Publicar estados de las articulaciones -->
        <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher" />
    
        <!-- Visualización en RViz con una configuración guardada -->
        <node name="rviz" pkg="rviz" type="rviz" args="-d $(find ur5_v1)/config/config.rviz" />
    
        <!-- GUI para mover juntas manualmente -->
        <arg name="use_gui" default="true" />
        <node name="joint_state_publisher" pkg="joint_state_publisher" type="joint_state_publisher" output="screen" unless="$(arg use_gui)" />
        <node name="joint_state_publisher_gui" pkg="joint_state_publisher_gui" type="joint_state_publisher_gui" output="screen" if="$(arg use_gui)"/>
    
    </launch>
    ```
✅ Paso 7 – Ejecutar RViz para guardar configuración personalizada
```
cd ~/catkin_ws
roslaunch ur5_v1 rviz_ur5.launch
```
Es probable que el robot no aparezca de inmediato. Realiza lo siguiente en RViz
- Fixed Frame → base_link
- GlobalOptions → Fixed Frame → base_link
- Grid → Plane Cell Count → 20
- Grid → Cell Size → 0.1
- En la pestaña Displays, haz clic en Add y añade:
  - RobotModel
  - TF
  - MotionPlanning
  
Una vez configurado todo, guarda la visualización:
```
cd ~/catkin_ws/src/ur5_v1
mkdir config
```
En RViz: File → Save Config → Guarda como config.rviz en la carpeta config que acabas de crear.


✅ Paso 8 – Crear archivo de configuración de controladores
1. Crear el archivo ur5_controllers.yaml
  ```
  cd ~/catkin_ws/src/ur5_v1/config
  touch ur5_controllers.yaml
  ```
2. Obtener el archivo base de configuración
   Busca este archivo:
   ```
   ~/catkin_ws/src/universal_robot/ur_gazebo/config/ur5_controller.yaml
   ```
   Copia todo su contenido y pégalo en tu archivo ur5_controllers.yaml.
4. Ajuste de namespace (muy importante)
Dado que nuestro namespace es ur5, modifica el archivo pegado para que toda la configuración esté anidada bajo ur5:. Ejemplo:
  ```
  ur5:
    joint_state_controller:
      type: joint_state_controller/JointStateController
      publish_rate: &loop_hz 125
  
    arm_controller:
      type: effort_controllers/JointTrajectoryController
      joints:
        - shoulder_pan_joint
        - shoulder_lift_joint
        - elbow_joint
        - wrist_1_joint
        - wrist_2_joint
        - wrist_3_joint
      gains:
        shoulder_pan_joint: {p: 100, d: 1, i: 1, i_clamp: 1}
        ...
  ```
  📝 Nota: JointTrajectoryController es usado por el plugin de RViz para ejecutar trayectorias.
  📝 Nota: El publish_rate alto (125 Hz) mejora la suavidad de la simulación. Puedes bajarlo a 50 Hz para pruebas ligeras.


✅ Paso 9 – Crear un mundo personalizado mínimo para Gazebo
1. Crear el archivo de mundo
  ```
  cd ~/catkin_ws/src/ur5_v1
  mkdir worlds
  cd worlds
  touch my_custom_world.world
  ```
2. Contenido del archivo my_custom_world.world

   Este mundo contiene el plano base, dos mesas y tres cubos de prueba:
   ```
   <?xml version="1.0" ?>
    <sdf version="1.6">
      <world name="default">
    
        <!-- Plano base y sol -->
        <include>
          <uri>model://ground_plane</uri>
        </include>
    
        <include>
          <uri>model://sun</uri>
        </include>
    
        <!-- Mesa debajo del UR5 -->
        <include>
          <uri>model://table</uri>
          <name>table1</name>
          <pose>0 0.30 0 0 0 0</pose>
        </include>
    
        <!-- Segunda mesa al lado derecho -->
        <include>
          <uri>model://table</uri>
          <name>table2</name>
          <pose>0 -0.5 0 0 0 0</pose>
        </include>
    
        <!-- Cubos estáticos de colores -->
        <model name="cube1">
          <static>true</static>
          <link name="link">
            <pose>0.30 0.50 1.04 0 0 0</pose>
            <visual name="visual">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
              <material><ambient>1 0 0 1</ambient></material>
            </visual>
            <collision name="collision">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
            </collision>
          </link>
        </model>
    
        <model name="cube2">
          <static>true</static>
          <link name="link">
            <pose>-0.50 0 1.04 0 0 0</pose>
            <visual name="visual">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
              <material><ambient>0 1 0 1</ambient></material>
            </visual>
            <collision name="collision">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
            </collision>
          </link>
        </model>
    
        <model name="cube3">
          <static>true</static>
          <link name="link">
            <pose>0 0.3 1.04 0 0 0</pose>
            <visual name="visual">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
              <material><ambient>0 0 1 1</ambient></material>
            </visual>
            <collision name="collision">
              <geometry><box><size>0.05 0.05 0.05</size></box></geometry>
            </collision>
          </link>
        </model>
    
      </world>
    </sdf>
   ```

✅ Paso 10 – Crear archivos launch para lanzar simulación y MoveIt
1. Crear los archivos launch
```
cd ~/catkin_ws/src/ur5_v1/launch
touch ur5_gazebo_w1_1.launch
touch ur5_moveit_with_rviz_1.launch
```
📦 Archivo ur5_gazebo_w1_1.launch

Este archivo lanza Gazebo con el UR5 en tu mundo personalizado y carga los controladores.
  ```
  <?xml version="1.0"?>
  <launch>
  
      <!-- Cargar modelo URDF desde xacro -->
      <param name="robot_description" command="$(find xacro)/xacro '$(find ur5_v1)/urdf/ur5_1.xacro'" />
  
      <!-- Posición del robot en el mundo -->
      <arg name="x" default="0" />
      <arg name="y" default="0" />
      <arg name="z" default="1.015" />
  
      <!-- Mundo personalizado -->
      <arg name="world_file" default="$(find ur5_v1)/worlds/my_custom_world.world" />
  
      <!-- Lanzar Gazebo con el mundo -->
      <include file="$(find gazebo_ros)/launch/empty_world.launch">
          <arg name="paused" value="false"/>
          <arg name="gui" value="true"/>
          <arg name="use_sim_time" value="true"/>
          <arg name="world_name" value="$(arg world_file)"/>
      </include>
  
      <!-- Publicador de estado del robot -->
      <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>
  
      <!-- Spawnear el robot -->
      <node name="spawn_the_robot" pkg="gazebo_ros" type="spawn_model"
            output="screen"
            args="-urdf -param robot_description -model ur5 -x $(arg x) -y $(arg y) -z $(arg z)" />
  
      <!-- Cargar y activar controladores -->
      <rosparam file="$(find ur5_v1)/config/ur5_controllers.yaml" command="load"/>
      <node name="controller_spawner" pkg="controller_manager" type="spawner"
            args="joint_state_controller eff_joint_traj_controller --timeout 60" />
  
  </launch>
  ```
🤖 Archivo ur5_moveit_with_rviz_1.launch
Este archivo lanza MoveIt, remapea controladores para Gazebo y abre RViz con tu configuración.
  ```
  <launch>
    <arg name="sim" default="true" />
    <arg name="debug" default="false" />
  
    <!-- Remapeo para usar controllers de Gazebo -->
    <remap if="$(arg sim)" from="/scaled_pos_joint_traj_controller/follow_joint_trajectory" to="/eff_joint_traj_controller/follow_joint_trajectory"/>
  
    <!-- Lanzar MoveIt -->
    <include file="$(find ur5_moveit_config)/launch/move_group.launch">
      <arg name="debug" value="$(arg debug)" />
    </include>
  
    <!-- Lanzar RViz con configuración -->
    <node name="rviz" pkg="rviz" type="rviz" output="screen"
          args="-d $(find ur5_v1)/config/config.rviz" />
  </launch>
  ```

▶️ Cómo lanzar la simulación
1. Terminal 1 – Lanzar Gazebo con el robot
  ```
  roslaunch ur5_v1 ur5_gazebo_w1_1.launch
  ```
2. Terminal 2 – Lanzar MoveIt + RViz
   Solo después de que Gazebo esté corriendo (reproducir si está pausado):
  ```
  roslaunch ur5_v1 ur5_moveit_with_rviz_1.launch
  ```
Recuerda: En el archivo de Gazebo, ya configuraste que inicie con paused="false", así que Gazebo debería estar listo para el segundo paso sin intervención.


✅ Paso 11. Visualización de la orientación (RPY) y posición en RViz

Para poder visualizar la orientación en RPY (radianes y grados) y la posición en RViz, utilizamos dos scripts de Python. Sigue estos pasos para configurarlo:

1. Crear la carpeta y los scripts
Crea una carpeta llamada scripts dentro de tu paquete ur5_v1 en ~/catkin_ws_6/src/ur5_v1 y agrega los siguientes scripts:
    - Crea los archivos rpy_marker_rad.py y rpy_marker_deg.py.
    - Asigna permisos de ejecución a los archivos con el siguiente comando:
    ```
    chmod +x rpy_marker_rad.py
    chmod +x rpy_marker_deg.py
    ```
    - Pega los códigos de los scripts que se detallan a continuación en cada archivo.

2. Ejecutar los scripts
Ejecuta los scripts en dos terminales diferentes:
  ```
  rosrun ur5_v1 rpy_marker_rad.py
  ```
  ```
  rosrun ur5_v1 rpy_marker_deg.py
  ```

3. Configuración en RViz
  - En RViz, agrega un nuevo marcador:
    - Ve a "Add" → "Marker"
    - En "MarkerTopic", selecciona /rpy_marker_rad o /rpy_marker_deg según corresponda.
  - Guarda tu configuración de RViz como config.rviz (no es necesario crear un nuevo archivo, solo guarda el que ya tenías).

Códigos de los scripts (buscar en el repositorio: src/ur5_v1/) 
- rpy_marker_rad.py 
- 

    
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅


```
```

---
## Conclusión
Este tutorial documenta todo el proceso necesario para simular el robot UR5 con un gripper Robotiq 85 en ROS, incluyendo la instalación de dependencias, la clonación de paquetes, la configuración de MoveIt y el lanzamiento correcto en Gazebo y RViz.

Gracias a esta guía, es posible tener un entorno funcional para pruebas con el UR5 en ROS, dejando todo listo para futuros desarrollos como scripts de movimiento, integración con visión, o secuencias de pick and place.

Además, se explicaron los archivos clave que deben modificarse, como los controladores, URDFs, y launch files, lo que ayuda a entender cómo se estructura un sistema completo de simulación con ROS.

## Referencias y Recursos Adicionales
- Enlace a documentación oficial:
https://wiki.ros.org/noetic

- Tutoriales relacionados:
https://ros-planning.github.io/moveit_tutorials/
http://wiki.ros.org/Industrial/Tutorials

- Repositorio de código fuente:
https://github.com/YeredBC/TURORIAL-ROS.git

## Contacto
- Asesor: Cesar Martinez Torres
  - 🔗 GitHub: https://github.com/cesar-martinez-torres/UDLAP_Robotics.git
  - 📧 Correo electrónico: cesar.martinez@udlap.mx

- Nombre: Juan Pablo Rosas Pineda:
  - 🔗 GitHub: https://github.com/RosasJP17
  - 📧 Correo electrónico: juan.rosaspa@udlap.mx
- Nombre: Cesar Maximiliano Gutierrez Velazquez
  - 📧 Correo electrónico: cesar.gutierrezvz@udlap.mx
- Nombre: Antonio De Jesus Xicali Arriaga
  - 🔗 GitHub: https://github.com/AntonioXicali101
  - 📧 Correo electrónico: antonio.xicaliaa@udlap.mx
- Nombre: Yered Yosshiel Bojorquez Castillo
  - 🔗 GitHub: https://github.com/YeredBC
  - 📧 Correo electrónico: yered.bojorquezco@udlap.mx
