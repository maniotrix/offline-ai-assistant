import { karna } from '../generated/messages';
import { CommandChannel } from './websocket/command-channel';
import { StatusChannel } from './websocket/status-channel';
import { ScreenCaptureChannel } from './websocket/screen-capture-channel';
import { ErrorHandler, MessageHandler } from './websocket/base-channel';

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

    onStatusUpdate(handler: MessageHandler<karna.status.IStatusResult>): () => void {
        return this.statusChannel.onStatusUpdate(handler);
    }

    onCommandResponse(handler: MessageHandler<karna.command.ICommandResult>): () => void {
        return this.commandChannel.onCommandResponse(handler);
    }

    onCaptureResponse(handler: MessageHandler<karna.screen_capture.ICaptureResult>): () => void {
        return this.screenCaptureChannel.onCaptureResponse(handler);
    }

    onError(handler: ErrorHandler): () => void {
        const unsubCommand = this.commandChannel.onError(handler);
        const unsubStatus = this.statusChannel.onError(handler);
        const unsubScreenCapture = this.screenCaptureChannel.onError(handler);
        return () => {
            unsubCommand();
            unsubStatus();
            unsubScreenCapture();
        };
    }
}

export const websocketService = new WebSocketService();