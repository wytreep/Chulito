import { AppService } from './app.service.js';

describe('AppService', () => {
  it('returns a synthetic health result without external services', () => {
    expect(new AppService().health()).toEqual({
      service: 'chulito-api',
      status: 'ok',
      synthetic: true,
    });
  });
});
