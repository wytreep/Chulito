import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  health() {
    return {
      service: 'chulito-api',
      status: 'ok',
      synthetic: true,
    } as const;
  }
}
