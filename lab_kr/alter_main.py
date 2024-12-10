from lab_kr.animations.directional_light_rotation_animation import DirectionalLightRotationAnimation
from lab_kr.camera import Camera
from lab_kr.light.directional_light import DirectionalLight
from lab_kr.materials.material import Material
from lab_kr.materials.textures import ImageTexture, FlatTexture
from lab_kr.particles.emitters.cone_emitter import ConeEmitter
from lab_kr.render_window import RenderWindow
from lab_kr.scene import Scene
from lab_kr.shapes.plane import Plane
from lab_kr.shapes.cone import Cone
from lab_kr.shapes.cube import Cube
from lab_kr.shapes.stl_model import StlModel


def main():
    # Создаем окно рендеринга
    window = RenderWindow(800, 600, b"Course Work with Cone Emitter")

    # Создаем сцену
    scene = Scene()

    # Создаем камеру
    camera = Camera(position=[0.0, 2.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=-20.0)
    scene.set_camera(camera)

    # Загрузка текстур
    texture_floor = ImageTexture("../data/textures/floor.jpg")
    texture_floor.load()

    texture_leafs = ImageTexture("../data/textures/leafs.png")
    texture_leafs.load()

    texture_sand = ImageTexture("../data/textures/sand.jpg")
    texture_sand.load()

    texture_glass = FlatTexture([255, 255, 255, 55])
    texture_glass.load()

    # Создаем направленный свет
    directional_light = DirectionalLight(direction=[-0.2, -1.0, -0.3],
                                         ambient=[0.05, 0.05, 0.05],
                                         diffuse=[0.9, 0.9, 0.9],
                                         specular=[0.8, 0.8, 0.8])
    scene.add_light(directional_light)

    # Создаем анимацию вращения направленного света
    light_animation = DirectionalLightRotationAnimation(light=directional_light,
                                                        axis=[0.0, 1.0, 0.5],  # Вращение вокруг Y-оси
                                                        speed=60.0)  # 60 градусов в секунду
    scene.add_animation(light_animation)
    light_animation.start()  # Запускаем анимацию

    # Создаем материал для пола
    floor_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.5, 0.5, 0.5],
        specular=[0.2, 0.2, 0.2],
        shininess=10.0,
        texture=texture_floor.texture_id,
        transparent=False
    )

    cone_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.5, 0.3],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture_sand.texture_id,
        transparent=True
    )

    sandwatch_material = Material(
        ambient=[0.1, 0.1, 0.1],
        diffuse=[0.8, 0.5, 0.3],
        specular=[0.5, 0.5, 0.5],
        shininess=32.0,
        texture=texture_glass.texture_id,
        transparent=True
    )

    # Создаем объект плоскости
    floor = Plane(position=[0.0, 0.0, 0.0], scale=40.0, rotation=[0.0, 0.0, 0.0], material=floor_material)
    scene.add_object(floor)

    cone = Cone(
        base_radius=1.0,
        height=2.0,
        slices=30,
        position=[0.0, 0.0, 0.0],
        rotation=[0.0, 0.0, 0.0],
        material=cone_material
    )
    scene.add_object(cone)

    cube = Cube(
        position=[0.0, 6.0, 0.0],
        scale=3,
        rotation=[0.0, 0.0, 0.0],
        material=cone_material
    )
    scene.add_object(cube)

    sandwatch = StlModel(
        stl_path="../data/models/hourglass.stl",
        position=[0.0, -10.0, 0.0],
        scale=0.1,
        rotation=[0.0, 41.0, -70.0],
        material=sandwatch_material
    )
    scene.add_object(sandwatch)

    # КУРСОВАЯ РАБОТА
    scene.initialize_particle_system()

    # Создаем эмиттер для конуса
    cone_emitter = ConeEmitter(
        position=cone.position,  # Позиция совпадает с вершиной конуса
        rotation=cone.rotation,  # Передаем поворот конуса
        emission_rate=50,
        max_particles=500,
        speed_range=(1.0, 3.0),  # Скорость частиц
        size_range=(3.4, 5.4),  # Размер частиц
        color=[205, 205, 160, 255],  # Красный цвет
        lifetime=3.0,
        base_radius=1.0,
        height=2.0
    )
    scene.add_emitter_to_particle_system(cone_emitter)

    # Устанавливаем сцену в окно рендеринга
    window.set_scene(scene)

    # Запускаем рендеринг
    window.run()


if __name__ == "__main__":
    main()