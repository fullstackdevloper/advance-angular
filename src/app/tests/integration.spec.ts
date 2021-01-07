TestBed.configureTestingModule({
  declarations: [AppComponent, BookListComponent, BookCollectionComponent],
  imports: [
    HttpClientTestingModule,
    StoreModule.forRoot({
      books: booksReducer,
      collection: collectionReducer,
    }),
  ],
  providers: [GoogleBooksService],
}).compileComponents();

fixture = TestBed.createComponent(AppComponent);
component = fixture.debugElement.componentInstance;

fixture.detectChanges();


describe('buttons should work as expected', () => {
  it('should add to collection when add button is clicked and remove from collection when remove button is clicked', () => {
    const addButton = getBookList()[1].query(
      By.css('[data-test=add-button]')
    );

    click(addButton);
    expect(getBookTitle(getCollection()[0])).toBe('Second Title');

    const removeButton = getCollection()[0].query(
      By.css('[data-test=remove-button]')
    );
    click(removeButton);

    expect(getCollection().length).toBe(0);
  });
});

//functions used in the above test
function getCollection() {
  return fixture.debugElement.queryAll(By.css('.book-collection .book-item'));
}

function getBookList() {
  return fixture.debugElement.queryAll(By.css('.book-list .book-item'));
}

function getBookTitle(element) {
  return element.query(By.css('p')).nativeElement.textContent;
}

function click(element) {
  const el: HTMLElement = element.nativeElement;
  el.click();
  fixture.detectChanges();
}