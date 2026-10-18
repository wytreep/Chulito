import { Body, Controller, Get, Post } from '@nestjs/common';
import { ApiOperation, ApiProperty, ApiTags } from '@nestjs/swagger';
import { IsString, Length } from 'class-validator';
import { AppService } from './app.service.js';

class EchoRequest {
  @ApiProperty({ example: 'synthetic-check' })
  @IsString()
  @Length(1, 80)
  message!: string;
}

@ApiTags('health')
@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get('health')
  @ApiOperation({ summary: 'Health check sintético del spike' })
  health() {
    return this.appService.health();
  }

  @Post('echo')
  @ApiOperation({ summary: 'Valida un payload sintético' })
  echo(@Body() body: EchoRequest) {
    return { message: body.message };
  }
}
