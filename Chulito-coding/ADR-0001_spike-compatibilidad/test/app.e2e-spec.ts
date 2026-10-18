import { INestApplication, ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import { App } from 'supertest/types.js';
import { AppModule } from '../src/app.module.js';
import { AppService } from '../src/app.service.js';

const appService = new AppService();

describe('Chulito API synthetic compatibility (e2e)', () => {
  let app: INestApplication<App>;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideProvider(AppService)
      .useValue(appService)
      .compile();

    app = moduleFixture.createNestApplication();
    app.setGlobalPrefix('api');
    app.useGlobalPipes(
      new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    );
    const config = new DocumentBuilder()
      .setTitle('Chulito compatibility spike')
      .setVersion('0.1.0')
      .build();
    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('api/docs', app, document);
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('serves the health endpoint through the Express adapter', async () => {
    await request(app.getHttpServer())
      .get('/api/health')
      .expect(200)
      .expect({ service: 'chulito-api', status: 'ok', synthetic: true });
  });

  it('validates payloads through the global ValidationPipe', async () => {
    await request(app.getHttpServer())
      .post('/api/echo')
      .send({ message: 'synthetic-check' })
      .expect(201)
      .expect({ message: 'synthetic-check' });

    await request(app.getHttpServer())
      .post('/api/echo')
      .send({ message: 123, unexpected: true })
      .expect(400);
  });

  it('serves the generated OpenAPI document', async () => {
    const response = await request(app.getHttpServer())
      .get('/api/docs-json')
      .expect(200);
    expect(response.body.info.title).toBe('Chulito compatibility spike');
    expect(response.body.paths['/api/health']).toBeDefined();
  });
});
