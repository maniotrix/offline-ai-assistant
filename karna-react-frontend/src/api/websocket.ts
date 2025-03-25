import { karna } from '../generated/messages';
import { CommandChannel } from './websocket/command-channel';
import { StatusChannel } from './websocket/status-channel';
import { ScreenCaptureChannel } from './websocket/screen-capture-channel';
import { VisionDetectChannel } from './websocket/vision-detect-channel';

class WebSocketService {
    private commandChannel: CommandChannel;
    private statusChannel: StatusChannel;
    private screenCaptureChannel: ScreenCaptureChannel;
    private visionDetectChannel: VisionDetectChannel;

    constructor() {
        this.commandChannel = new CommandChannel();
        this.statusChannel = new StatusChannel();
        this.screenCaptureChannel = new ScreenCaptureChannel();
        this.visionDetectChannel = new VisionDetectChannel();
    }

    connect(): void {
        this.commandChannel.connect();
        this.statusChannel.connect();
        this.screenCaptureChannel.connect();
        this.visionDetectChannel.connect();
    }

    disconnect(): void {
        this.commandChannel.disconnect();
        this.statusChannel.disconnect();
        this.screenCaptureChannel.disconnect();
        this.visionDetectChannel.disconnect();
    }

    async sendCommand(command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> {
        return this.commandChannel.sendCommand(command, domain);
    }

    async requestStatus(): Promise<void> {
        return this.statusChannel.requestStatus();
    }

    async startScreenCapture(projectUuid: string, commandUuid: string): Promise<void> {
        return this.screenCaptureChannel.startCapture(projectUuid, commandUuid);
    }

    async stopScreenCapture(projectUuid: string, commandUuid: string): Promise<void> {
        return this.screenCaptureChannel.stopCapture(projectUuid, commandUuid);
    }

    async updateScreenCapture(projectUuid: string, commandUuid: string, updatedEvents: any[]): Promise<void> {
        return this.screenCaptureChannel.updateCapture(projectUuid, commandUuid, updatedEvents);
    }

    async getCaptureCache(projectUuid: string, commandUuid: string): Promise<void> {
        return this.screenCaptureChannel.getCache(projectUuid, commandUuid);
    }

    async getVisionDetectResults(
        projectUuid: string, 
        commandUuid: string, 
        screenshotEvents: karna.screen_capture.IRpcScreenshotEvent[]
    ): Promise<void> {
        return this.visionDetectChannel.getResults(projectUuid, commandUuid, screenshotEvents);
    }

    async updateVisionDetectResults(results: karna.vision.IVisionDetectResultsList): Promise<void> {
        return this.visionDetectChannel.updateResults(results);
    }
}

export const websocketService = new WebSocketService();