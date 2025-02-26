import { karna } from '../generated/messages';
import { CommandChannel } from './websocket/command-channel';
import { StatusChannel } from './websocket/status-channel';
import { ErrorHandler, MessageHandler } from './websocket/base-channel';

class WebSocketService {
    private commandChannel: CommandChannel;
    private statusChannel: StatusChannel;

    constructor() {
        this.commandChannel = new CommandChannel();
        this.statusChannel = new StatusChannel();
    }

    connect(): void {
        this.commandChannel.connect();
        this.statusChannel.connect();
    }

    disconnect(): void {
        this.commandChannel.disconnect();
        this.statusChannel.disconnect();
    }

    async sendCommand(command: string, domain: string = 'default'): Promise<karna.command.ICommandResult> {
        return this.commandChannel.sendCommand(command, domain);
    }

    async requestStatus(): Promise<void> {
        return this.statusChannel.requestStatus();
    }

    onStatusUpdate(handler: MessageHandler<karna.status.IStatusResult>): () => void {
        return this.statusChannel.onStatusUpdate(handler);
    }

    onCommandResponse(handler: MessageHandler<karna.command.ICommandResult>): () => void {
        return this.commandChannel.onCommandResponse(handler);
    }

    onError(handler: ErrorHandler): () => void {
        const unsubCommand = this.commandChannel.onError(handler);
        const unsubStatus = this.statusChannel.onError(handler);
        return () => {
            unsubCommand();
            unsubStatus();
        };
    }
}

export const websocketService = new WebSocketService();