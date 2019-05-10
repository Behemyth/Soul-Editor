#include "Editor.h"

Editor::Editor(SoulParameters params) :
	SoulApplication(params) {

}

int main(int, char*[])
{
	//app params
	SoulParameters appParams;
	Editor app(appParams);

	//create the window
	WindowParameters windowParams;
	windowParams.type = WindowType::BORDERLESS;
	windowParams.title = "Main";
	windowParams.monitor = 0;
	windowParams.pixelPosition.x = 0;
	windowParams.pixelPosition.y = 0;
	windowParams.pixelSize.x = 512;
	windowParams.pixelSize.y = 512;

	app.CreateWindow(windowParams);

	//SetWindowLayout(mainWindow, new SingleLayout(new RenderWidget()));


	app.Run();

}