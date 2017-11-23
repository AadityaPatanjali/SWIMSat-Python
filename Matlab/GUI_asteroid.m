function varargout = GUI_asteroid(varargin)
% GUI_ASTEROID MATLAB code for GUI_asteroid.fig
%      GUI_ASTEROID, by itself, creates a new GUI_ASTEROID or raises the existing
%      singleton*.
%
%      H = GUI_ASTEROID returns the handle to a new GUI_ASTEROID or the handle to
%      the existing singleton*.
%
%      GUI_ASTEROID('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI_ASTEROID.M with the given input arguments.
%
%      GUI_ASTEROID('Property','Value',...) creates a new GUI_ASTEROID or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before GUI_asteroid_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to GUI_asteroid_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help GUI_asteroid

% Last Modified by GUIDE v2.5 03-Aug-2017 14:43:20

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @GUI_asteroid_OpeningFcn, ...
                   'gui_OutputFcn',  @GUI_asteroid_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before GUI_asteroid is made visible.
function GUI_asteroid_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to GUI_asteroid (see VARARGIN)

% Choose default command line output for GUI_asteroid
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);
set(handles.radius_text,'String',get(handles.radius,'Value'));
set(handles.speed_text,'String',get(handles.speed,'Value'));
set(handles.brightness_text,'String',get(handles.brightness,'Value'));
set(handles.loop_text,'String',get(handles.loop,'Value'));
set(handles.R_text,'String',get(handles.R,'Value'));
set(handles.G_text,'String',get(handles.G,'Value'));
set(handles.B_text,'String',get(handles.B,'Value'));
R1 = get(handles.R,'Value');
G1 = get(handles.G,'Value');
B1 = get(handles.B,'Value');
circle(0,0,1,R1,G1,B1);
% UIWAIT makes GUI_asteroid wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = GUI_asteroid_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on slider movement.
function radius_Callback(hObject, eventdata, handles)
% hObject    handle to radius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
radius_val = get(hObject,'Value');
set(handles.radius_text,'String',num2str(radius_val));

% --- Executes during object creation, after setting all properties.
function radius_CreateFcn(hObject, eventdata, handles)
% hObject    handle to radius (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function speed_Callback(hObject, eventdata, handles)
% hObject    handle to speed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
speed_val = get(hObject,'Value');
set(handles.speed_text,'String',num2str(speed_val));

% --- Executes during object creation, after setting all properties.
function speed_CreateFcn(hObject, eventdata, handles)
% hObject    handle to speed (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function brightness_Callback(hObject, eventdata, handles)
% hObject    handle to brightness (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
brightness_val = get(hObject,'Value');
set(handles.brightness_text,'String',num2str(brightness_val));

% --- Executes during object creation, after setting all properties.
function brightness_CreateFcn(hObject, eventdata, handles)
% hObject    handle to brightness (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
a = get(handles.radius,'Value');
b = get(handles.brightness,'Value');
c = get(handles.speed,'Value');
n = get(handles.loop,'Value');
R = get(handles.R,'Value');
G = get(handles.G,'Value');
B = get(handles.B,'Value');
asteroid_graphics(a,c,b,n,R,G,B)


% --- Executes on slider movement.
function loop_Callback(hObject, eventdata, handles)
% hObject    handle to loop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
loop_val = get(hObject,'Value');
set(handles.loop_text,'String',num2str(loop_val));

% --- Executes during object creation, after setting all properties.
function loop_CreateFcn(hObject, eventdata, handles)
% hObject    handle to loop (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function R_Callback(hObject, eventdata, handles)
% hObject    handle to R (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
R_val = get(hObject,'Value');
set(handles.R_text,'String',num2str(R_val));
R1 = get(handles.R,'Value');
G1 = get(handles.G,'Value');
B1 = get(handles.B,'Value');
circle(0,0,1,R1,G1,B1);

% --- Executes during object creation, after setting all properties.
function R_CreateFcn(hObject, eventdata, handles)
% hObject    handle to R (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function G_Callback(hObject, eventdata, handles)
% hObject    handle to G (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
G_val = get(hObject,'Value');
set(handles.G_text,'String',num2str(G_val));
R1 = get(handles.R,'Value');
G1 = get(handles.G,'Value');
B1 = get(handles.B,'Value');
circle(0,0,1,R1,G1,B1);

% --- Executes during object creation, after setting all properties.
function G_CreateFcn(hObject, eventdata, handles)
% hObject    handle to G (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function B_Callback(hObject, eventdata, handles)
% hObject    handle to B (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
B_val = get(hObject,'Value');
set(handles.B_text,'String',num2str(B_val));
R1 = get(handles.R,'Value');
G1 = get(handles.G,'Value');
B1 = get(handles.B,'Value');
circle(0,0,1,R1,G1,B1);

% --- Executes during object creation, after setting all properties.
function B_CreateFcn(hObject, eventdata, handles)
% hObject    handle to B (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end
