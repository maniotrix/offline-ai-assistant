import { karna } from '../generated/messages';
import { CommandChannel } from './websocket/command-channel';
import { StatusChannel } from './websocket/status-channel';
import { ScreenCaptureChannel } from './websocket/screen-capture-channel';

class WebSocketService {
    private commandChannel: CommandChannel;
    private statusChannel: StatusChannel;
    private screenCaptureChannel: ScreenCaptureChannel;

    constructor() {
        this.commandChannel = new CommandChannel();
        this.statusChannel = new StatusChannel();
        this.screenCaptureChannel = new ScreenCaptureChannel();
    }

    connect(): void {
        this.commandChannel.connect();
        this.statusChannel.connect();
        this.screenCaptureChannel.connect();
    }

    disconnect(): void {
        this.commandChannel.disconnect();
        this.statusChannel.disconnect();
        this.screenCaptureChannel.disconnect();
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

    async updateScreenCapture(projectUuid: string, commandUuid: string, deletedEventIds: string[]): Promise<void> {
        return this.screenCaptureChannel.updateCapture(projectUuid, commandUuid, deletedEventIds);
    }

    async getCaptureCache(projectUuid: string, commandUuid: string): Promise<void> {
        return this.screenCaptureChannel.getCache(projectUuid, commandUuid);
    }
}

export const websocketService = new WebSocketService();