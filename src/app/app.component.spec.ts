import { TestBed, async } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        AppComponent
      ],
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'GrugeRetort'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('GrugeRetort');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement;
    expect(compiled.querySelector('.content span').textContent).toContain('GrugeRetort app is running!');
  });
});


mockBooksSelector.setResult([
  {
    id: 'firstId',
    volumeInfo: {
      title: 'First Title',
      authors: ['First Author'],
    },
  },
  {
    id: 'secondId',
    volumeInfo: {
      title: 'Second Title',
      authors: ['Second Author'],
    },
  },
]);

mockBookCollectionSelector.setResult([
  {
    id: 'firstId',
    volumeInfo: {
      title: 'First Title',
      authors: ['First Author'],
    },
  },
]);

store.refreshState();
fixture.detectChanges();

expect(
  fixture.debugElement.queryAll(By.css('.book-list .book-item')).length
).toBe(2);

expect(
  fixture.debugElement.queryAll(By.css('.book-collection .book-item'))
    .length
).toBe(1);
