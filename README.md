# filament_analyzer v.0.0.2
A simple analyzer for filamentation images / Анализатор изображений филаментов

Филамент — нитевидная структура, образующаяся при распространении лазерного импульса в нелинейной среде. Данная программа анализирует поперечные изображения филаментов. 

Реализованные возможности:

1) фильтр кадров без сигнала и с "зашкалом"

	На вход программы подаётся путь, указывающий на директорию, содержащую текстовые файлы для обработки (каждый файл содержит двумерный массив чисел типа integer). Название текстовых файлов задано в виде *_*.txt
	
	Файлы для тестирования: ./data/filter_examples

	Результат работы программы:

	Файлы с "зашкалом" перемещаются в директорию ./overscaled/;
	файлы с недостаточным сигналом — ./weak/

	В директории также могут находится готовые тепловые карты, соответствующие текстовым файлам. Если для конкретного файла с зашкалом/недостаточным сигналом такая карта есть, её также необходимо переместить (при этом в имени картинки присутствуют дополнительные параметры, их необходимо сохранить). Если нет — необходимо построить.
	
Возможности, которые ещё могут быть реализованы:

2) очищение от шумов (усреднение) и построение тепловых карт продольных изображений люминесценции $N2$ в филаменте

	На вход программы подаётся путь, указывающий на директорию, содержащую бинарные файлы для обработки (первые четыре пикселя несут информацию о размере изображения в пикселях "0 1920 0 1200", дальше информация сгруппирована по пиксельно, на каждый пиксель — два бита). Название входных файлов задано в виде *.dat.
	
	Файлы для тестирования: ./data/lumin_examples
	
	Результат работы программы:
	
	Считываются бинарные файлы, затем присходит усреднение по полю изображения (в продольном направлении) методом бегущего среднего и вычитается фон. Для очищенного изображения строится тепловая карта и записывается в директорию с результатами: ./out_data/out_lumin_examples
----------------------

3) фильтр кадров с "пробоями" (на изображении нет чётких пиков — нет филамента)

4) подсчет количества максимумов (число филаментов в суперфиламенте).

----------------------------------------

Исполнитель: Василий Пушкарев

Постановка задачи: Д.В. Пушкарев, кафедра общей физики и волновых процессов,
[puschkarev.dmitriy@physics.msu.ru](puschkarev.dmitriy@physics.msu.ru) 
