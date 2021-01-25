bl_info = {
    'name': 'Creator music visualization',
    'description': 'The simple tool to create music visualization from an MP3 file',
    'author': "Piotr 'Piter' Krupa",
    'version': (1, 0, 0),
    'blender': (2, 91, 0),
    'location': 'View3D > UI > Visualizations',
    'warning': 'Is working only in Windows',
    'category': 'Tools' }
    
#Importowanie modułów dostępnych w Pythonie od Blendera
import bpy
import math
import os
import time

from bpy.types import PropertyGroup, Operator, Panel
from bpy.props import StringProperty, EnumProperty, FloatVectorProperty, PointerProperty


#Klasa do tworzenia wizualizacji muzyki:
class Visualization_Music:
   
    #Importowanie i inicjalizacja danych do wykorzystania w kilku metodach
    def __init__(self,FileMP3,FileObject,FrameRate): 
        
        #Czyszczenie sceny przed wizualizacją:
        #Sprawdzamy czy scena jest czysta czy nie
        if bpy.context.scene.objects.get('Cube') or bpy.context.scene.objects.get('Camera') or bpy.context.scene.objects.get('Light'):
            
            #Zaznacz wszystko 
            bpy.ops.object.select_all(action='SELECT')
            
            #Usuwanie obiektów z sceny 
            bpy.ops.object.delete()

            #Czyszczenie danych o istniejących wcześniej obiektach na scenie (domyślnie to kamera, kostka i światło)
            bpy.data.cameras.remove(camera = bpy.data.cameras['Camera']) 
            bpy.data.meshes.remove(mesh=bpy.data.meshes['Cube'])         
            bpy.data.lights.remove(light=bpy.data.lights['Light'])     
        
        #Inicjalizacja danych:
        #Import obiektu 'COWM.obj' na scene
        bpy.ops.import_scene.obj(filepath=FileObject, use_groups_as_vgroups=True, split_mode='OFF') 

        #Ścieżka do pliku w formacie MP3
        self.FileMP3 = FileMP3
        
        #Nazwa muzyki MP3 (Potrzebne do czyszczenia danych po zakończeniu renderingu)
        self.NameFileMP3 = os.path.basename(FileMP3)

        #Częstotliwości                                               
        self.Freqs = [[0,250],[250,500],[500,750],[750,1000]]

        #Dostęp do obiektu (kuli z emiterami). Ustawiamy pozycje w jednej z osi i odznaczamy obiekt 
        self.Obj = bpy.data.objects['COWM']  
        self.Obj.location[2] = 4                                          
        self.Obj.select_set(False)

        #Dostęp do sceny, gdzie znajdą się elementy do renderingu
        self.scene = bpy.data.scenes['Scene']
        
        #Ustawienie predkości animacji na 60 klatek na sekunde
        self.scene.render.fps = FrameRate

        #Wywołanie konsoli w celu ukazania postępów w renderingu + wyczyszczenie jej i wyświetlenie komunikatu       
        bpy.ops.wm.console_toggle()
        os.system('cls')
        print('The data has been loaded.\nThe scene has been cleared.\nThe object has been imported.')
        print('\nThe visualization is being prepared for rendering.\nPlease wait!')

    
    #Zmiana koloru tła sceny na wybrany przez użytkownika (tryb Viewport Shading)
    def Background_Prepare(self,ColorBackground):
        
        #Dostęp do parametrów World. Zmiana wartości parametrów w node Background (Color i Strength)
        W = bpy.data.worlds['World'] 
        W.node_tree.nodes['Background'].inputs[0].default_value = ColorBackground
        W.node_tree.nodes['Background'].inputs[1].default_value = 0.1
        
        #Komunikat o wykonaniu metody
        print('\nThe background for visualization is ready!')
    
    #Dodanie muzyki do edytora sekwencji (Video Sequencer)
    def Music_Prepare(self):
        
        #Wykreowanie edytora sekwencji, jesli nie jest prawidłowy lub nie istnieje                                                             
        if not self.scene.sequence_editor:                                             
            self.scene.sequence_editor_create()

        #Dodanie muzyki do edytora sekwencji (Nazwa do wywołania, ścieżka do pliku MP3, kanał, Od której klatki odtwarzamy)                                         
        self.scene.sequence_editor.sequences.new_sound('Music',self.FileMP3,0,1)
        
        #Komunikat o wykonaniu metody
        print('The music is ready! ')


    #Dodanie systemu cząsteczek, przygotowanie animacji cząstek  
    def Particle_Systems_Prepare(self):
        
        #Informacja o długości muzyki (liczba klatek)
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            lifetime = 50
            timestep = 0.2
        elif(self.scene.render.fps > 30):
            lifetime = 100
            timestep = 0.1

        #Dodaj Particle system (Dodajemy modyfikator do obiektu)
        for i in range(0,4):
            self.Obj.modifiers.new('P'+str(i+1), type='PARTICLE_SYSTEM')     
    
            #Dodajemy obiekt, który będzie kształtem cząstki. Zmieniamy nazwę i umieszczamy ją poza pole widzenia kamery
            bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1)            
            bpy.data.objects['Icosphere'].name = 'P'+str(i+1)                
            bpy.data.objects['P'+str(i+1)].location = [1500,1500,1500]             
            
        #Odznacz ostatnią stworzoną, by prawidłowo obsłużyć każdy z emiterów
        bpy.data.objects['P4'].select_set(False)                         

        #Dodajemy materiał z jakiego będą miały cząstki z danego emitera (czerwony, niebieski, zielony, biały to kolory domyślne)
        bpy.data.objects['P1'].active_material = bpy.data.materials['RED_EMITER']   
        bpy.data.objects['P2'].active_material = bpy.data.materials['BLUE_EMITER']
        bpy.data.objects['P3'].active_material = bpy.data.materials['GREEN_EMITER']
        bpy.data.objects['P4'].active_material = bpy.data.materials['WHITE_EMITER']

        #Zaznaczamy obiekt, który posiada Particle Systems 
        self.Obj.select_set(True)
        
        #Pętla do ustawiania parametrów cząstek
        for i in range(0,4):
            #Emission
            bpy.data.particles['P'+str(i+1)].count = 2500                                            #Liczba cząstek
            bpy.data.particles['P'+str(i+1)].frame_start = 1                                         #Pierwsza klatka animacji
            bpy.data.particles['P'+str(i+1)].frame_end = MP3DataFrame                                #Ostatnia klatka animacji
            bpy.data.particles['P'+str(i+1)].lifetime = lifetime                                     #Czas życia cząstek
            
            #Emission -> Source
            bpy.data.particles['P'+str(i+1)].use_emit_random = False                                 #Wyłącz Random Order
            bpy.data.particles['P'+str(i+1)].use_even_distribution = False                           #Wyłącz Even Distribution
            
            #Velocity
            bpy.data.particles['P'+str(i+1)].normal_factor = 0.25                                    #Zmiana wartości normal (prędkość cząstek we wszystkich kierunkach)
            bpy.data.particles['P'+str(i+1)].tangent_factor = 0.05                                   #Niech styczna do powierzchni da cząstce prędkość początkową                                  
            bpy.data.particles['P'+str(i+1)].tangent_phase = 1                                       #Obróć powierzchnię styczną
            bpy.data.particles['P'+str(i+1)].object_align_factor[0] = -1.20                          #Prędkość w osi X
            
            #Physics -> Integration
            bpy.data.particles['P'+str(i+1)].timestep = timestep                                     #Krok czasowy                                         
            
            #Render
            bpy.data.particles['P'+str(i+1)].render_type = 'OBJECT'                                  #Typ Obiektu jako kształt cząstek                                  
            bpy.data.particles['P'+str(i+1)].particle_size = 0.150                                   #Wielkość cząstek
            bpy.data.particles['P'+str(i+1)].instance_object = bpy.data.objects['P'+str(i+1)]        #Wybieramy obiekt jako kształt cząstek
            
            #Field Weights
            bpy.data.particles['P'+str(i+1)].effector_weights.gravity = 0                            #Wartość siły grawitacji                         
            
            #Children -> Simple
            bpy.data.particles['P'+str(i+1)].child_type = 'SIMPLE'                                   #Dzielimy cząstki na grupy 'dzieci'\'rodziców'. Wybieramy metodę SIMPLE
            bpy.data.particles['P'+str(i+1)].child_nbr = 30                                          #Liczba 'dzieci'\'rodziców' do wyświetlenia
            bpy.data.particles['P'+str(i+1)].rendered_child_count = 50                               #Liczba 'dzieci'\'rodziców' do renderingu                                                                                                        
            bpy.data.particles['P'+str(i+1)].child_radius = 0.5                                     #Odległość dzieci od rodziców
            bpy.data.particles['P'+str(i+1)].clump_factor = -1                                       #Tworzenie 'chmur' z grup cząstek
    
            bpy.data.particles['P'+str(i+1)].keyframe_insert(data_path='child_size')                 #Rozmiar cząstek dzieci jako klatki kluczowe                 
    
            #Przetwarzanie Krzywej F na bazie fali dźwiękowej
    
            area = bpy.context.area     #Pobranie informacji o aktualnej przestrzeni w GUI Blendera                                   
            area_type = area.type       #Pobranie typu przestrzeni w GUI Blendera                                
            area.type = 'GRAPH_EDITOR'  #Przejście do przestrzeni: 'Edytor wykresów'                               
    
            #Tworzenie animacji z krzywej na bazie muzyki (Bake sound to F-Curve)
            bpy.ops.graph.sound_bake(filepath=self.FileMP3, low=self.Freqs[i][0], high=self.Freqs[i][1])
            
            #Odznaczenie już przetworzonej krzywej
            bpy.data.particles['P'+str(i+1)].animation_data.action.fcurves[0].select = False   
    
            area.type = area_type #Przejście z powrotem do poprzedniej przestrzeni w GUI Blendera
    
            #Vertex Groups
            self.Obj.particle_systems['P'+str(i+1)].vertex_group_density = 'Emiter'+str(i+1) #Ustaw vertex_group jako emiter (Grupa wierzchołków jako miejsce skąd wylatują cząstki)

        #Po zakonczeniu przetwarzania krzywych odznaczamy obiekt z system cząsteczkowym    
        self.Obj.select_set(False)
        
        #Komunikat o wykonaniu metody
        print('The particle systems is ready!')


#Przygotowanie materiałów do animacji    
    def Emission_Prepare(self,ColorEmission):
        
        #Zaznaczamy obiekt, ktory posiada materiały do przetworzenia  
        self.Obj.select_set(True)

        #Ustawienie Parametrów (kolor emisji i siłe emisji):
        bpy.data.materials['RED_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission'].default_value = ColorEmission[0]
        bpy.data.materials['BLUE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission'].default_value = ColorEmission[1]
        bpy.data.materials['GREEN_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission'].default_value = ColorEmission[2]
        bpy.data.materials['WHITE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission'].default_value = ColorEmission[3]
        bpy.data.materials['GOLD'].node_tree.nodes['Principled BSDF'].inputs['Emission'].default_value = ColorEmission[4]
        
        bpy.data.materials['RED_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3.500
        bpy.data.materials['BLUE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3.500
        bpy.data.materials['GREEN_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3.500
        bpy.data.materials['WHITE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 3.500
        bpy.data.materials['GOLD'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 2.000

        #Dostęp do parametru 'Emission Strength' w 'Principled BSDF'
        RED = bpy.data.materials['RED_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']    
        BLUE = bpy.data.materials['BLUE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']   
        GREEN = bpy.data.materials['GREEN_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']  
        WHITE = bpy.data.materials['WHITE_EMITER'].node_tree.nodes['Principled BSDF'].inputs['Emission Strength']

        
        #Ustawienie czerwonego Emitera:
        #Zaznacz wejście 'Emission Strength' jako klatkę kluczową
        RED.keyframe_insert(data_path='default_value') 

        #Wybierz odpowiednią krzywą i zaznacz
        bpy.data.materials['RED_EMITER'].node_tree.animation_data.action.fcurves[0].select = True

        #Przetwarzanie Krzywej F na bazie fali dźwiękowej
        area = bpy.context.area     #Pobranie informacji o aktualnej przestrzeni w GUI Blendera                                    
        area_type = area.type       #Pobranie typu przestrzeni w GUI Blendera                                        
        area.type = 'GRAPH_EDITOR'  #Przejście do przestrzeni: 'Edytor wykresów' 

        #Tworzenie animacji z krzywej na bazie muzyki (Bake sound to F-Curve)
        bpy.ops.graph.sound_bake(filepath=self.FileMP3, low=self.Freqs[0][0], high=self.Freqs[0][1])
        
        #Odznaczenie już przetworzonej krzywej  
        bpy.data.materials['RED_EMITER'].node_tree.animation_data.action.fcurves[0].select = False      
        
        area.type = area_type #Przejście z powrotem do poprzedniej przestrzeni w GUI Blendera


        #Ustawienie niebieskiego Emitera:
        #Zaznacz wejście 'Emission Strength' jako klatkę kluczową
        BLUE.keyframe_insert(data_path='default_value') 

        #Wybierz odpowiednią krzywą i zaznacz
        bpy.data.materials['BLUE_EMITER'].node_tree.animation_data.action.fcurves[0].select = True

        #Przetwarzanie Krzywej F na bazie fali dźwiękowej
        area = bpy.context.area     #Pobranie informacji o aktualnej przestrzeni w GUI Blendera                                    
        area_type = area.type       #Pobranie typu przestrzeni w GUI Blendera                                        
        area.type = 'GRAPH_EDITOR'  #Przejście do przestrzeni: 'Edytor wykresów' 

        #Tworzenie animacji z krzywej na bazie muzyki (Bake sound to F-Curve)
        bpy.ops.graph.sound_bake(filepath=self.FileMP3, low=self.Freqs[1][0], high=self.Freqs[1][1])
        
        #Odznaczenie już przetworzonej krzywej  
        bpy.data.materials['BLUE_EMITER'].node_tree.animation_data.action.fcurves[0].select = False      
        
        area.type = area_type #Przejście z powrotem do poprzedniej przestrzeni w GUI Blendera


        #Ustawienie zielonego Emitera:
        #Zaznacz wejście 'Emission Strength' jako klatkę kluczową
        GREEN.keyframe_insert(data_path='default_value') 

        #Wybierz odpowiednią krzywą i zaznacz
        bpy.data.materials['GREEN_EMITER'].node_tree.animation_data.action.fcurves[0].select = True

        #Przetwarzanie Krzywej F na bazie fali dźwiękowej
        area = bpy.context.area     #Pobranie informacji o aktualnej przestrzeni w GUI Blendera                                    
        area_type = area.type       #Pobranie typu przestrzeni w GUI Blendera                                        
        area.type = 'GRAPH_EDITOR'  #Przejście do przestrzeni: 'Edytor wykresów' 

        #Tworzenie animacji z krzywej na bazie muzyki (Bake sound to F-Curve)
        bpy.ops.graph.sound_bake(filepath=self.FileMP3, low=self.Freqs[2][0], high=self.Freqs[2][1])
        
        #Odznaczenie już przetworzonej krzywej  
        bpy.data.materials['GREEN_EMITER'].node_tree.animation_data.action.fcurves[0].select = False      
        
        area.type = area_type #Przejście z powrotem do poprzedniej przestrzeni w GUI Blendera
        

        #Ustawienie Białego Emitera:
        #Zaznacz wejście 'Emission Strength' jako klatkę kluczową
        WHITE.keyframe_insert(data_path='default_value') 

        #Wybierz odpowiednią krzywą i zaznacz
        bpy.data.materials['WHITE_EMITER'].node_tree.animation_data.action.fcurves[0].select = True

        #Przetwarzanie Krzywej F na bazie fali dźwiękowej
        area = bpy.context.area     #Pobranie informacji o aktualnej przestrzeni w GUI Blendera                                    
        area_type = area.type       #Pobranie typu przestrzeni w GUI Blendera                                        
        area.type = 'GRAPH_EDITOR'  #Przejście do przestrzeni: 'Edytor wykresów' 

        #Tworzenie animacji z krzywej na bazie muzyki (Bake sound to F-Curve)
        bpy.ops.graph.sound_bake(filepath=self.FileMP3, low=self.Freqs[3][0], high=self.Freqs[3][1])
        
        #Odznaczenie już przetworzonej krzywej  
        bpy.data.materials['WHITE_EMITER'].node_tree.animation_data.action.fcurves[0].select = False      
        
        area.type = area_type #Przejście z powrotem do poprzedniej przestrzeni w GUI Blendera

        #Po zakonczeniu przetwarzania krzywych odznaczamy obiekt z materialami    
        self.Obj.select_set(False)

        #Komunikat o wykonaniu metody
        print('The emission colors is ready!')

    #Dodanie kamery do sceny i ustawienie jej parametrów
    def Camera_Prepare(self):
        
        #Informacja o długośći muzyki (liczba klatek)
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration 

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            frames = [0,75,175,100,200,100]
        elif(self.scene.render.fps > 30):
            frames = [0,150,350,200,400,200]

        if not self.scene.objects.get('Camera'):
            #Pozycja kamery na scenie, Obrót kamery, Skala kamery
            camera_pos = (10, 0, 0)                                                                                                          
            camera_rot = (math.radians(90),math.radians(0),math.radians(-90))                      
            camera_sca = (1,1,1)

            #Dodanie kamery na scene                                                                   
            bpy.ops.object.camera_add(location=camera_pos, rotation=camera_rot, scale=camera_sca)     
        
        #Wybór używanej kamery na scenie
        self.scene.camera = bpy.data.objects['Camera']

        #Wybrane parametry kamery(Długość ogniskowej, głębia ostrości, skupienie na obiekcie)                                      
        bpy.data.cameras['Camera'].lens = 25                                                   
        bpy.data.cameras['Camera'].dof.use_dof = True                                          
        bpy.data.cameras['Camera'].dof.focus_object = self.Obj

        #Do kamery dobieramy modyfikator 'ograniczenia' 'TRACK TO' by śledziła ona obiekt na scenie ('COWN.obj')
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.data.objects['Camera'].constraints['Track To'].target = self.Obj 

        #Przygotowujemy animację ruchu kamery w konkretnych momentach wizualizacji (Początek, Twist, Zakończenie)
        #Ustawiamy wskaźnik na osi czasu na konkretną klatkę, wprowadzamy nową pozycję kamery, następnie zapisujemy pozycję
        #jako klatkę kluczową
        self.scene.frame_set(frames[0])
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        
        self.scene.frame_set(frames[1])
        bpy.data.objects['Camera'].location = [0,-10,4]
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        
        self.scene.frame_set(frames[2])
        bpy.data.objects['Camera'].location = [-18.5,0,4]
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
       
        self.scene.frame_set(MP3DataFrame//2 - frames[3])
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        
        self.scene.frame_set(MP3DataFrame//2)
        bpy.data.objects['Camera'].location = [-22,0,4]
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        
        self.scene.frame_set(MP3DataFrame - frames[4])
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        
        self.scene.frame_set(MP3DataFrame - frames[5])
        bpy.data.objects['Camera'].location = [-17.5,0,4]
        bpy.data.objects['Camera'].keyframe_insert(data_path='location')
        self.scene.frame_set(1)
        
        bpy.data.objects['Camera'].select_set(False)

        #Komunikat o wykonaniu metody
        print('The camera is ready!')

    #Przygotowanie Luster, które posłużą do twistu (Odbicia lustrzane od obiektu)
    def Mirrors_Prepare(self,ColorMirrors):

        #Informacja o długośći muzyki (liczba klatek)
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            frames = [0,100,200,100]
        elif(self.scene.render.fps > 30):
            frames = [0,200,400,200]

        #Pozycje luster i ich rotacja
        location_Mirrors_Animation = [(-5,0,0.3),(-5,-6.5,4),(-5,6.5,4),(-5,0,7.7),(3,0,4)]
        rotation_Mirrors_Animation = [
                                        (math.radians(0),math.radians(0),math.radians(0)),
                                        (math.radians(90),math.radians(0),math.radians(0)),
                                        (math.radians(90),math.radians(0),math.radians(0)),
                                        (math.radians(0),math.radians(0),math.radians(0)),
                                        (math.radians(0),math.radians(-90),math.radians(0))  
                                    ]

        #Tworzymy nowy materiał, ustawiamy Metallic ('Metaliczność') i Roughness('Chropowatość') tak by stworzyć powierzchnie lustrzaną                     
        bpy.data.materials.new('MIRROR')
        bpy.data.materials['MIRROR'].use_nodes = True
        bpy.data.materials['MIRROR'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = ColorMirrors
        bpy.data.materials['MIRROR'].node_tree.nodes['Principled BSDF'].inputs['Metallic'].default_value = 1
        bpy.data.materials['MIRROR'].node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0  
        
        #Tworzymy Plane, którę będą powierzchniami lustrzanymi. Nadajemy im podstawowe parametry, zmieniamy nazwę i dodajemy materiał
        for i in range(0,5):
            bpy.ops.mesh.primitive_plane_add(size=16, location=location_Mirrors_Animation[i], rotation=rotation_Mirrors_Animation[i])
            bpy.data.objects['Plane'].name = 'Mirror'+str(i+1)
            bpy.data.objects['Mirror'+str(i+1)].scale = [0,0,0]
            bpy.data.objects['Mirror'+str(i+1)].active_material = bpy.data.materials['MIRROR']
            
        #Odznaczam ostatni stworzony Plane by lepiej kontrolować animację luster
        bpy.data.objects['Mirror5'].select_set(False)    
        
        #Przygotowujemy animację luster. Po przez zmianę parametru scale będą się pojawiać i znikać podczas wizualizacji
        #Ustawiamy wskaźnik na osi czasu na konkretną klatkę, wprowadzamy nowy scale kamery, następnie zapisujemy pozycję
        #jako klatkę kluczową
        self.scene.frame_set(frames[0])
        for i in range(0,5):
            bpy.data.objects['Mirror'+str(i+1)].keyframe_insert(data_path='scale')
        
        self.scene.frame_set(MP3DataFrame//2 - frames[1])
        for i in range(0,5):
            bpy.data.objects['Mirror'+str(i+1)].scale = [0,0,0]
            bpy.data.objects['Mirror'+str(i+1)].keyframe_insert(data_path='scale')
        
        self.scene.frame_set(MP3DataFrame//2)
        for i in range(0,5):
            bpy.data.objects['Mirror'+str(i+1)].scale = [1,1,1]
            bpy.data.objects['Mirror'+str(i+1)].keyframe_insert(data_path='scale')
        
        self.scene.frame_set(MP3DataFrame-frames[2])
        for i in range(0,5):
            bpy.data.objects['Mirror'+str(i+1)].keyframe_insert(data_path='scale')
        
        self.scene.frame_set(MP3DataFrame-frames[3])
        for i in range(0,5):
            bpy.data.objects['Mirror'+str(i+1)].scale = [0,0,0]
            bpy.data.objects['Mirror'+str(i+1)].keyframe_insert(data_path='scale')

        self.scene.frame_set(1)

        #Komunikat o wykonaniu metody
        print('The mirrors is ready!')

    #Przygotowanie animacji zakończenia wizualizacji muzyki jako eksplozji obiektu.
    def Ending_Prepare(self, ColorExplosion):
        
        #Informacja o długośći muzyki (liczba klatek)
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            frames = [1,5,18,23,28]
            frame_S_E = 40
            lifetime = 55
        elif(self.scene.render.fps > 30):
            frames = [1,10,35,45,55]
            frame_S_E = 80
            lifetime = 110

        #Ustawienie Particle Systems
        self.Obj.modifiers.new('Explosion', type='PARTICLE_SYSTEM')

        #Emission
        bpy.data.particles['Explosion'].count = 2500
        bpy.data.particles['Explosion'].frame_start = MP3DataFrame + frame_S_E
        bpy.data.particles['Explosion'].frame_end = MP3DataFrame + frame_S_E
        bpy.data.particles['Explosion'].lifetime = lifetime

        #Velocity
        bpy.data.particles['Explosion'].normal_factor = 1
        bpy.data.particles['Explosion'].factor_random = 25 #Randomowa prędkość każdej cząstki (W normal mamy od 0 do 1 m/s)

        #Render
        bpy.data.particles['Explosion'].render_type = 'NONE'

        #Field Weights
        bpy.data.particles['Explosion'].effector_weights.gravity = 0

        #Modyfikator Explode. Pozwoli nam na wykorzystanie Particle Systems do eksplozji obiektu
        self.Obj.modifiers.new('ExplodeObject', type='EXPLODE')
        self.Obj.modifiers['ExplodeObject'].particle_uv = 'UVMap'
        self.Obj.modifiers['ExplodeObject'].use_edge_cut = True


        #Dodanie światła, ustawienie parametrów jak pozycja, obrót i skala, zmiana nazwy obiektu światła
        if not bpy.context.scene.objects.get('Light'):
            light_pos = (0, 0, 4)                                                                            
            light_rot = (0, 0, 0)                                                                            
            light_sca = (1, 1, 1)                                                                            
            bpy.ops.object.light_add(type='POINT', location=light_pos, rotation=light_rot, scale=light_sca)  
            bpy.data.objects['Point'].name = 'Light'
            bpy.data.lights['Point'].color = ColorExplosion                                                         
    
            #Animacja coraz mocniej święcącego się światła.
            #Ustawiamy wskaźnik na osi czasu na konkretną klatkę, zmieniamy moc święcenia (Power/energy w Watach), następnie zapisujemy
            #wartość parametru jako klatkę kluczową
            self.scene.frame_set(frames[0])   
            bpy.data.lights['Point'].energy = 0
            bpy.data.lights['Point'].keyframe_insert(data_path='energy')
            
            self.scene.frame_set(MP3DataFrame - frames[1])
            bpy.data.lights['Point'].keyframe_insert(data_path='energy')
            
            self.scene.frame_set(MP3DataFrame + frames[2])
            bpy.data.lights['Point'].energy = 10000
            bpy.data.lights['Point'].keyframe_insert(data_path='energy')
            
            self.scene.frame_set(MP3DataFrame + frames[3])
            bpy.data.lights['Point'].energy = 250000
            bpy.data.lights['Point'].keyframe_insert(data_path='energy')
            
            self.scene.frame_set(MP3DataFrame + frames[4])
            bpy.data.lights['Point'].energy = 300000
            bpy.data.lights['Point'].keyframe_insert(data_path='energy')
            
            self.scene.frame_set(1)
        
        #Komunikat o wykonaniu metody
        print('The ending is ready!')
    
    #Zaprogramowanie animacji obrotu obiektu w jednej osi i wychyleń obiektu w drugiej osi
    def Rotation_Object_Prepare(self,Direction_rotation):

        #Informacja o długośći muzyki (liczba klatek)
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            frame_step = 35
            rotation_speed = 3.50
        elif(self.scene.render.fps > 30):
            frame_step = 75
            rotation_speed = 1.75

        #Pętla do tworzenia animacji wychyleń obiektu o 7.5 stopnia w jedną i drugą stronę w jednej osi.
        #W tym przypadku osi Z. od 1 do ostatniej klatki muzyki co 55 klatek. Sprawdzamy czy numer klatki
        #jest liczbą parzystą czy nie i ustalamy wartość wychylenia obiektu.
        for i in range(1,MP3DataFrame,frame_step):
            self.scene.frame_set(i)
            if(i%2==0):
                self.Obj.rotation_euler[2] = math.radians(7.5)
                self.Obj.keyframe_insert(data_path='rotation_euler', index = 2)
            else:
                self.Obj.rotation_euler[2] = math.radians(-7.5)
                self.Obj.keyframe_insert(data_path='rotation_euler', index = 2) 
        
        #Pętle do tworzenia animacji obrotu obiektu w jednej osi w jedną stronę (w pierwszej połowie muzyki)
        #i w drugą (w drugiej połowie muzyki). W tym przypadku w osi X. W zależności do wartośći Direction_rotation
        #ustalany jest kolejność kierunków obrotu.
        for i in range(1,MP3DataFrame//2):
            self.scene.frame_set(i)
            
            if Direction_rotation == True:
                self.Obj.rotation_euler[0] += rotation_speed*math.pi/180
            else:
                self.Obj.rotation_euler[0] += -rotation_speed*math.pi/180
            
            self.Obj.keyframe_insert(data_path='rotation_euler', index = 0)
        
        for i in range((MP3DataFrame//2),MP3DataFrame):
            self.scene.frame_set(i)
            
            if Direction_rotation == True:
                self.Obj.rotation_euler[0] += -rotation_speed*math.pi/180
            else:
                self.Obj.rotation_euler[0] += rotation_speed*math.pi/180
            
            self.Obj.keyframe_insert(data_path='rotation_euler', index = 0)

        #Ustawienie pozycji końcowej obiektu po zakończeniu animacji obrotu i wychyleń obiektu 
        self.scene.frame_set(MP3DataFrame)
        self.Obj.rotation_euler[0] = math.radians(0)
        self.Obj.rotation_euler[2] = math.radians(0)
        self.Obj.keyframe_insert(data_path='rotation_euler', index = 0)
        self.Obj.keyframe_insert(data_path='rotation_euler', index = 2)
                    
        self.scene.frame_set(1)

        #Komunikat o wykonaniu metody
        print('The object rotation is ready!')

    #Przygotowanie i wykonanie renderingu wizualizacji muzyki na silniku EEVEE
    def Render_Animation(self, Resolution, FileSave, NameFile, Quality, SampleRate):

        #Informacja o długośći muzyki (liczba klatek) 
        MP3DataFrame = self.scene.sequence_editor.sequences_all['Music'].frame_final_duration

        #Sprawdzamy jako liczbę FPS podano i ustawiamy odpowiednie parametry
        if(self.scene.render.fps <= 30):
            Number_frames = MP3DataFrame + 95   
        elif(self.scene.render.fps > 30):
            Number_frames = MP3DataFrame + 190    
    
        #Ustawiamy długośc trwania całej powstałej wizualizacji
        self.scene.frame_start = 1    
        self.scene.frame_end = Number_frames    
        self.scene.frame_step = 1 
        
        #Włączenie efektów Bloom i parametr jego intesywności (Pozwala to na świecenie obiektów z kolerem emission) oraz
        #Screen Space Reflections (odbicia w obiektach z materiałem lustrzanym) w trybie EEVEE 
        self.scene.eevee.use_bloom = True
        self.scene.eevee.bloom_intensity = 0.1
        self.scene.eevee.use_ssr = True

        #Ustawienie rozdzielczości renderu
        self.scene.render.resolution_x = Resolution[0]
        self.scene.render.resolution_y = Resolution[1]
        self.scene.render.resolution_percentage = 100

        #Ustawienia czy plik ma mieć automatyczne rozszerzenie z liczbą klatek w tytule,
        #nazwy pliku wideo, formatu pliku, formatu wideo, kodeku wideo i kodeku audio, 
        #jakość renderingu, częstotliwość próbkowania audio, kanałów audio 
        self.scene.render.use_file_extension = False
        self.scene.render.filepath = FileSave + NameFile + '.mp4' 
        self.scene.render.image_settings.file_format = 'FFMPEG'                    
        self.scene.render.ffmpeg.format = 'MPEG4'                                                   
        self.scene.render.ffmpeg.codec = 'H264'                                                     
        self.scene.render.ffmpeg.audio_codec = 'MP3' 
        self.scene.render.ffmpeg.constant_rate_factor = Quality  
        self.scene.render.ffmpeg.audio_mixrate = SampleRate 
        self.scene.render.ffmpeg.audio_channels = 'STEREO'                                              
    
        #Podanie informacji do konsoli ile klatek trzeba wyrenderować
        print('\n\nThe number of frames to be rendered: ' + str(Number_frames) + '\n')
        
        #Konsola czeka 5 sekund i potem rozpocznie się rendering
        time.sleep(5)
        
        #Rozpoczęcie renderingu
        bpy.ops.render.render(animation=True)

        #Podanie informacji o zakończeniu renderowania wizualizacji 
        print('\n\nThe visualization is ready!')
        print('\nEnjoy listening and watching !')
        
        #Konsola czeka 5 sekund aż zostanie zamknięta
        time.sleep(5)

        #Wyłączenie konsoli po zakończeniu renderingu        
        bpy.ops.wm.console_toggle()


    #Usuwanie obiektów ze sceny i czyszczenie danych po zakończeniu renderingu
    def Clear_After_Visualization(self):
        
        #Usuwanie muzyki
        self.scene.sequence_editor_clear()
        
        #Usuniecie Obiektów, Luster, Kamery, Swiatla ze sceny
        bpy.ops.object.select_all(action='SELECT') #Zaznacz wszystko 
        bpy.ops.object.delete() #Usuwanie obiektów znajdujac się na scenie
        
        #Czyszczenie danych o obiektach, kamerach, materiałach, animacjach, muzyce i particle systems.
        bpy.data.cameras.remove(camera = bpy.data.cameras['Camera'])
        bpy.data.lights.remove(light = bpy.data.lights['Point'])
        bpy.data.sounds.remove(sound = bpy.data.sounds[str(self.NameFileMP3)])
            
        bpy.data.materials.remove(material=bpy.data.materials['RED_EMITER'])
        bpy.data.materials.remove(material=bpy.data.materials['BLUE_EMITER'])
        bpy.data.materials.remove(material=bpy.data.materials['GREEN_EMITER'])
        bpy.data.materials.remove(material=bpy.data.materials['WHITE_EMITER'])
        bpy.data.materials.remove(material=bpy.data.materials['GOLD'])
        bpy.data.materials.remove(material=bpy.data.materials['MIRROR'])
        
        bpy.data.meshes.remove(mesh=bpy.data.meshes['COWM'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Icosphere'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Icosphere.001'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Icosphere.002'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Icosphere.003'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Plane'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Plane.001'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Plane.002'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Plane.003'])
        bpy.data.meshes.remove(mesh=bpy.data.meshes['Plane.004'])
        
        bpy.data.particles.remove(particle = bpy.data.particles['P1'])
        bpy.data.particles.remove(particle = bpy.data.particles['P2'])
        bpy.data.particles.remove(particle = bpy.data.particles['P3'])
        bpy.data.particles.remove(particle = bpy.data.particles['P4'])
        bpy.data.particles.remove(particle = bpy.data.particles['Explosion'])   
        
        bpy.data.actions.remove(action = bpy.data.actions['COWMAction'])
        bpy.data.actions.remove(action = bpy.data.actions['CameraAction'])
        bpy.data.actions.remove(action = bpy.data.actions['PointAction'])
        bpy.data.actions.remove(action = bpy.data.actions['Mirror1Action'])
        bpy.data.actions.remove(action = bpy.data.actions['Mirror2Action'])
        bpy.data.actions.remove(action = bpy.data.actions['Mirror3Action'])
        bpy.data.actions.remove(action = bpy.data.actions['Mirror4Action'])
        bpy.data.actions.remove(action = bpy.data.actions['Mirror5Action'])
        bpy.data.actions.remove(action = bpy.data.actions['P1Action'])
        bpy.data.actions.remove(action = bpy.data.actions['P2Action'])
        bpy.data.actions.remove(action = bpy.data.actions['P3Action'])
        bpy.data.actions.remove(action = bpy.data.actions['P4Action'])
        bpy.data.actions.remove(action = bpy.data.actions['Shader NodetreeAction'])
        bpy.data.actions.remove(action = bpy.data.actions['Shader NodetreeAction.001'])
        bpy.data.actions.remove(action = bpy.data.actions['Shader NodetreeAction.002'])
        bpy.data.actions.remove(action = bpy.data.actions['Shader NodetreeAction.003']) 



#Właśćiwość/argumenty wykorzystywane przez operator: Wybór opcji, scieżki do plikow
class SettingsProperty(PropertyGroup):
    
    #ścieżka do pliku w formacie MP3
    File_MP3 : StringProperty(
    name = 'MP3',
    description = 'The path to MP3 audio file to read',
    subtype = 'FILE_PATH'
    )
    
    #ścieżka do zapisu wyrenderowanej wizualizacji
    File_Save : StringProperty(
    name = 'Save',
    description = 'The path to save vizualization',
    subtype = 'FILE_PATH'
    )

    #Ścieżka do obiektu wykorzystywanego do wizualizacji
    File_Object : StringProperty(
    name = 'Object',
    description = 'The path to load the object',
    subtype = 'FILE_PATH'
    )
            
    #Nazwa pliku wideo wizualizacji
    Name_VM : StringProperty(
    name = 'Name',
    description = 'The name wideo file the music visualization',
    default = 'Music Visualization'
    )
    
    #Kolorystyka użyta do obiektu wizualizacji muzyki
    Colors_VM : EnumProperty(
    name = 'Object',
    description = 'The choice of color palette for the object',
    items = [
             ('#1','RBGWG','The basic color palette (red, blue, green, white, gold)','COLORSET_01_VEC',1),
             ('#2','80s','The color palette inspired by the 80s (shades of pink + dark blue)','COLORSET_11_VEC',2),
             ('#3','Xmas','The color palette referring to Christmas (shades of colors red, green and white )','COLORSET_03_VEC',3),
             ('#4','Winter','The color palette referring to the winter (shades of gray, white and blue)','COLORSET_13_VEC',4),
             ('#5','Gold','The color palette shades of gold','COLORSET_09_VEC',5),
             ('#6','White&Red','The color palette white and red','COLORSET_01_VEC',6),
             ('#7','PYBGR','The color palette inspired by the Power rangers (pink, yellow, green, blue, red','COLORSET_05_VEC',7),
             ('#8','Fire','The color palette referring to the element of fire (warm colors: yellow, orange, brown, red)','COLORSET_02_VEC',8),
             ('#9','Water','The color palette referring to the element of water (cold colors: shades of blue)','COLORSET_04_VEC',9),
             ('#10','Metal Music','The color palette referring to metal music (grayscale)','COLORSET_10_VEC',10)
            ],
    default = '#1'
    )
    
    #Kolor tła
    Colors_Background_VM : FloatVectorProperty(
    name = 'Background',
    description = 'The choice of the background color',
    subtype='COLOR',
    min=0, 
    max=0.5,
    size=4, 
    default=[0.0,0.0,0.0,1]
    )
    
    #Kolor luster
    Colors_Mirrors_VM : FloatVectorProperty(
    name = 'Mirrors',
    description = 'The choice of color for the mirrors',
    subtype='COLOR',
    min=0, 
    max=1,
    size=4, 
    default=[1.0,1.0,1.0,1]
    )
    
    #Kolor światła eksplozji
    Colors_Explosion_VM : FloatVectorProperty(
    name = 'Explosion',
    description = 'The choice of color for the explosion effect',
    subtype='COLOR',
    min=0, 
    max=1,
    size=3, 
    default=[1.0,1.0,1.0]
    )

    #Wybór kierunku animacji obrotu obiektu
    Direction_Rotation_Object_VM : EnumProperty(
    name = 'Object',
    description = 'The choice of direction animation object rotation ',
    items = [
             ('#1','Clockwise','The right direction of object rotation',1),
             ('#2','Counter clockwise','The left direction of object rotation',2)
            ],
    default = '#1'  
    )
    
    #Rozdzielczość
    Resolution_VM : EnumProperty(
    name = 'Resolution',
    description = 'The choice of resolution for music visualization',
    items = [
             ('#1','480p','Resolution VGA (640x480).\nWarning: Visualization in this resolution may be in low quality!'),
             ('#2','600p','Resolution SVGA (800x600).\nWarning: Visualization in this resolution may be in low quality!'),
             ('#3','720p','Resolution HD (1280×720)'),
             ('#4','1080p','Resolution Full HD (1920x1080)'),
             ('#5','1440p','Resolution 1440p (2560x1440)'),
             ('#6','4K','Resolution 4K (4096 x 2160)')
            ],
    default = '#3'
    )
    
    #Jakość renderingu
    Quality_VM : EnumProperty(
    name = 'Quality',
    description = 'The choice of quality level render music visuazaliton',
    items = [
              ('#1','Lowest','The lowest quality'),
              ('#2','Very Low','The very low quality'),
              ('#3','Low','The low quality'),
              ('#4','Medium','The medium quality'),
              ('#5','High','The high quality'),
              ('#6','Perceptually Lossless','The perceptually lossless quality'),
              ('#7','Lossless','The lossless quality')
            ],
    default = '#4'
    )

    #Liczba klatek na sekunde
    Frame_Rate_VM : EnumProperty(
    name = 'Frame Rate',
    description = 'The choice of amount frames per second',
    items = [
              ('#1','30','30 FPS'),
              ('#2','60','60 FPS')
            ],
    default = '#1'
    )
    
    #Częstotliwość probkowania muzyki
    Sample_Rate_VM : EnumProperty(
    name = 'Sample Rate',
    description = 'The choice of amount sample rate in Hz.',
    items = [
              ('#1','44100 Hz','44100 Hz - the default value'),
              ('#2','48000 Hz','48000 Hz')
            ],
    default = '#1'
    )
    
    
#Operator - funkcjonalność Blender GUI - Panel
class VMAddon_OT_Operator(Operator):
    bl_idname = 'visualization.music'
    bl_label = 'Operator\Functionality for creating music visualization'
    bl_description = 'Operator\Functionality for creating music visualization'

    
    #Funkcja wykonania: Co ma zrobić operator
    def execute(self, context):
        #Wykorzystanie parametrów string i enum
        SettingsProperty = bpy.context.scene.SettingsProperty
        
        #Obiekty jako kontenery danych
        Col_PS_E = []
        Direction_rotation = False
        Resolution = []
        Quality = ''
        FrameRate = 0
        SampleRate = 0
        
        #Kontrola błędów. Sprawdzamy czy nie są puste pola odpowiedzialne za wczytanie pliku MP3,
        #ścieżki do zapisu wizualizacji i wczytanie obiektu do wizualizacji ('COWM.obj')
        if (not SettingsProperty.File_MP3 or not SettingsProperty.File_Save or not SettingsProperty.File_Object): 
            self.report({'ERROR'},'No path to MP3 file or to save the visualization or to the object is given')
            return {'CANCELLED'}
        
        #Sprawdzenie czy załadowano plik w formacie .mp3
        elif(not SettingsProperty.File_MP3.endswith('.mp3')):
            self.report({'ERROR'},'The given file is not in MP3 format. Please enter the path to the MP3 file')
            return {'CANCELLED'}
        
        #Sprawdzenie czy ścieżka do zapisu jest ścieżką do folderu, a nie pliku
        elif(not os.path.isdir(SettingsProperty.File_Save)):
            self.report({'ERROR'},'The path with the file is given. Please specify the path to the folder to save the video file')
            return {'CANCELLED'}
        
        #Sprawdzenie czy załadowany plik jest plik z obiektem 'COWM.obj'
        elif(os.path.basename(SettingsProperty.File_Object) != 'COWM.obj'):
            self.report({'ERROR'},'A different object than COWM.obj is given. Please load COWM.obj. file')
            return {'CANCELLED'}

        #Sprawdzenie czy użytkownik nie pozostawił pustego pola w nazwie pliku
        elif(not SettingsProperty.Name_VM):
            self.report({'ERROR'},'No name is given for saving the file')
            return {'CANCELLED'}
        
        else:
            #Sprawdzamy jaka kolorystyke wybrał uzytkownik
            if SettingsProperty.Colors_VM == '#1':
                
                #czerwony, niebieski, zielony, biały, złoty #Emiter1, Emiter2, Emiter3, Emiter4, Reszta Obiektu
                Col_PS_E.append([1,0,0,1])
                Col_PS_E.append([0,0,1,1])
                Col_PS_E.append([0,1,0,1])
                Col_PS_E.append([1,1,1,1])
                Col_PS_E.append([0.581,0.489,0,1])
            
            elif SettingsProperty.Colors_VM == '#2':
                
                #odcienie Rozowego, Fioletowego i Blekitny 
                Col_PS_E.append([0.514918,0.057805,0.887923,1])
                Col_PS_E.append([0.009359,0.736756,1,1])
                Col_PS_E.append([0.514918,0.057805,0.887923,1])
                Col_PS_E.append([0.009359,0.736756,1,1])
                Col_PS_E.append([0.256156,0.041693,1,1])
            
            elif SettingsProperty.Colors_VM == '#3':
                
                #odcień czerwonego, odcienie zielonego i biały
                Col_PS_E.append([1,0,0,1])
                Col_PS_E.append([0,0.450,0.025,1])
                Col_PS_E.append([0.630,0.686,0.693,1])
                Col_PS_E.append([0.102,0.171,0.000,1])
                Col_PS_E.append([1,1,1,1])
            
            elif SettingsProperty.Colors_VM == '#4':
                
                #odcienie szarości, bieli i niebieskiego
                Col_PS_E.append([0.871,0.887,0.887,1])
                Col_PS_E.append([0.082,0.208,0.381,1])
                Col_PS_E.append([0.102,0.191,0.262,1])
                Col_PS_E.append([0.630,0.686,0.693,1])
                Col_PS_E.append([0.230,0.396,0.520,1])
            
            elif SettingsProperty.Colors_VM == '#5':
                
                #odcienie Złotego
                Col_PS_E.append([0.887923,0.617207,0.01096,1])
                Col_PS_E.append([0.381326,0.116971,0.003035,1])
                Col_PS_E.append([0.520996,0.223228,0.005605,1])
                Col_PS_E.append([0.520996,0.341914,0.116971,1])
                Col_PS_E.append([0.693872,0.396755,0.01033,1])
                
            elif SettingsProperty.Colors_VM == '#6':

                #biały i czerwony
                Col_PS_E.append([1,1,1,1])
                Col_PS_E.append([1,0,0,1])
                Col_PS_E.append([1,1,1,1])
                Col_PS_E.append([1,0,0,1])
                Col_PS_E.append([1,0.212231,0.215861,1])

            elif SettingsProperty.Colors_VM == '#7':

                #Różowy, Żółty, niebieski, zielony, czerwony
                Col_PS_E.append([0.514918,0.057805,0.887923,1])
                Col_PS_E.append([1,0.791298,0,1])
                Col_PS_E.append([0,0.502887,1,1])
                Col_PS_E.append([0,0.708376,0.008023,1])
                Col_PS_E.append([1,0,0,1])

            elif SettingsProperty.Colors_VM == '#8':
                
                #Żółty, Jasny Pomarańczowy, Ciemny Pomarańczowy, czerwony, Brązowy
                Col_PS_E.append([0.887923,0.597202,0.001518,1])
                Col_PS_E.append([0.887923,0.242281,0.001518,1])
                Col_PS_E.append([0.693872,0.046665,0.001214,1])
                Col_PS_E.append([0.381326,0.005605,0.000911,1])
                Col_PS_E.append([0.019382,0.000304,0.000304,1])

            elif SettingsProperty.Colors_VM == '#9':

                #odcienie niebieskiego od Jasnego do Ciemnego
                Col_PS_E.append([0.132868,0.693872,0.610496,1])
                Col_PS_E.append([0.004777,0.423268,0.520996,1])
                Col_PS_E.append([0.003035,0.250158,0.381326,1])
                Col_PS_E.append([0.002428,0.135633,0.262251,1])
                Col_PS_E.append([0.002428,0.102242,0.262251,1])
                
            elif SettingsProperty.Colors_VM == '#10':
                
                #odcienie szarosć od białego do czarnego
                Col_PS_E.append([0.693872,0.693872,0.693872,1])
                Col_PS_E.append([0.262251,0.262251,0.262251,1])
                Col_PS_E.append([0.099899,0.099899,0.099899,1])
                Col_PS_E.append([0.06803,0.06803,0.06803,1])
                Col_PS_E.append([0.004025,0.004025,0.004025,1])

            #Sprawdzamy co użytkownik wybrał w opcjach wyboru kierunku animacji obrotu obiektu:
            if SettingsProperty.Direction_Rotation_Object_VM == '#1':
                Direction_rotation = True
            elif SettingsProperty.Direction_Rotation_Object_VM == '#2':
                Direction_rotation = False

            
            #Sprawdzamy co użytkownik wybrał w opcjach rozdzielczości:
            if SettingsProperty.Resolution_VM == '#1':
                Resolution.append(640)
                Resolution.append(480)
            elif SettingsProperty.Resolution_VM == '#2':
                Resolution.append(800)
                Resolution.append(600)  
            elif SettingsProperty.Resolution_VM == '#3':
                Resolution.append(1280)
                Resolution.append(720)
            elif SettingsProperty.Resolution_VM == '#4':
                Resolution.append(1920)
                Resolution.append(1080)
            elif SettingsProperty.Resolution_VM == '#5':
                Resolution.append(2560)
                Resolution.append(1440)
            elif SettingsProperty.Resolution_VM == '#6':
                Resolution.append(4096)
                Resolution.append(2160)

            
            #Sprawdzamy co użytkownik wybrał w opcjach jakości:
            if SettingsProperty.Quality_VM == '#1':
                Quality = 'LOWEST'
            elif SettingsProperty.Quality_VM == '#2':
                Quality = 'VERYLOW'
            elif SettingsProperty.Quality_VM == '#3':
                Quality = 'LOW'
            elif SettingsProperty.Quality_VM == '#4':
                Quality = 'MEDIUM'
            elif SettingsProperty.Quality_VM == '#5':
                Quality = 'HIGH'
            elif SettingsProperty.Quality_VM == '#6':
                Quality = 'PERC_LOSSLESS'
            elif SettingsProperty.Quality_VM == '#7':
                Quality = 'LOSSLESS'


            #Sprawdzamy co użytkownik wybrał w opcjach liczby klatek na sekunde:
            if SettingsProperty.Frame_Rate_VM == '#1':
                FrameRate = 30
            elif SettingsProperty.Frame_Rate_VM == '#2':
                FrameRate = 60
                
            
            #Sprawdzamy co użytkownik wybrał w opcjach czestotliwości próbkowania
            if SettingsProperty.Sample_Rate_VM == '#1':
                SampleRate = 44100
            elif SettingsProperty.Sample_Rate_VM =='#2':
                SampleRate = 48000


            #Uruchomienie metod odpowiedzialnych za stworzenie wizualizacji:
            VM = Visualization_Music(SettingsProperty.File_MP3, SettingsProperty.File_Object, FrameRate)
            VM.Background_Prepare(SettingsProperty.Colors_Background_VM)
            VM.Music_Prepare()
            VM.Particle_Systems_Prepare()
            VM.Emission_Prepare(Col_PS_E)
            VM.Camera_Prepare()
            VM.Mirrors_Prepare(SettingsProperty.Colors_Mirrors_VM)
            VM.Ending_Prepare(SettingsProperty.Colors_Explosion_VM)
            VM.Rotation_Object_Prepare(Direction_rotation)
            VM.Render_Animation(Resolution, SettingsProperty.File_Save, SettingsProperty.Name_VM, Quality, SampleRate)
            VM.Clear_After_Visualization()

            #Komunikat o lokalizacji pliku wideo
            self.report({'INFO'}, 'The visualization is available in : ' + str(SettingsProperty.File_Save))
            return {'FINISHED'}
        

#Panel - GUI Blendera
class VMAddon_PT_Panel(Panel):
    bl_idname = 'VMADDON_PT_panel'
    bl_label = 'Music Visualization'
    bl_description = 'The UI panel for music visualization operator (UI_OP)'
    bl_category = 'Visualization'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self,context):
        layout = self.layout
        
        #Instacja, w której przechowujemy dane
        SettingsProperty = bpy.context.scene.SettingsProperty
  
        #Etykieta z tekstem i z ikonką + pole do wprowadzenia danych.
        layout.label(text='The path to MP3 file', icon='FILE_SOUND')
        layout.prop(SettingsProperty,'File_MP3')
        
        layout.label(text='The path to save the visualization', icon='FILE_FOLDER')
        layout.prop(SettingsProperty,'File_Save')

        layout.label(text='Select COWM.obj object', icon='CUBE')
        layout.prop(SettingsProperty,'File_Object')
        
        layout.label(text='The name file video', icon='FILE_TEXT')
        layout.prop(SettingsProperty,'Name_VM')  
        
        #Separator
        layout.separator()
        
        layout.label(text='The colors object', icon='COLOR')
        layout.prop(SettingsProperty,'Colors_VM')
        
        layout.label(text='The color background scene', icon='COLOR')
        layout.prop(SettingsProperty,'Colors_Background_VM')
        
        layout.label(text='The color mirrors', icon='COLOR')
        layout.prop(SettingsProperty,'Colors_Mirrors_VM')
        
        layout.label(text='The color explosion', icon='COLOR')
        layout.prop(SettingsProperty,'Colors_Explosion_VM')
        
        layout.label(text='The direction object rotation', icon='LOOP_FORWARDS')
        layout.prop(SettingsProperty,'Direction_Rotation_Object_VM')
        
        layout.separator()
        
        layout.label(text='Resolution', icon='IMAGE_DATA')
        layout.prop(SettingsProperty,'Resolution_VM')
        
        layout.label(text='Quality', icon='IMAGE_DATA')
        layout.prop(SettingsProperty,'Quality_VM')
        
        layout.label(text='Frame rate', icon='IMAGE_DATA')
        layout.prop(SettingsProperty,'Frame_Rate_VM')
        
        layout.label(text='Sample rate', icon='SOUND')
        layout.prop(SettingsProperty,'Sample_Rate_VM')
                
        layout.separator()
        
        #Wprowadzenie przycisku do wykonania operacji
        row = layout.row()
        row.scale_y = 2
        row.scale_x = 1
        row.operator('visualization.music', text = 'RENDER VISUALIZATION', icon ='RENDER_RESULT')


#register jest funkcją, która działa tylko po włączeniu addona, co oznacza, że ​​moduł można załadować bez aktywacji addona
def register():
    bpy.utils.register_class(SettingsProperty)
    bpy.utils.register_class(VMAddon_OT_Operator)
    bpy.utils.register_class(VMAddon_PT_Panel)

    bpy.types.Scene.SettingsProperty = PointerProperty(type = SettingsProperty)

#unregister jest funkcją wyładowującą wszystko, co zostało ustawione przez rejestr, wywoływaną, gdy dodatek jest wyłączony.
def unregister():
    bpy.utils.unregister_class(SettingsProperty)
    bpy.utils.unregister_class(VMAddon_OT_Operator)
    bpy.utils.unregister_class(VMAddon_PT_Panel)
    
    del bpy.types.Scene.SettingsProperty
    
if __name__ == '__main__':
    register()