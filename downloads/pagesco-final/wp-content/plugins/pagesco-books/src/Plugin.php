<?php
/**
 * The plugin's main object.
 *
 * @package PagesCo\Books
 */

namespace PagesCo\Books;

/**
 * Starts the plugin's features and keeps them reachable.
 */
final class Plugin {

	/**
	 * The one instance, created on first use.
	 *
	 * @var Plugin|null
	 */
	private static ?Plugin $instance = null;

	/**
	 * The running features, keyed by class name.
	 *
	 * @var array<class-string, Feature>
	 */
	private array $features = array();

	/**
	 * Returns the plugin's one instance.
	 */
	public static function instance(): Plugin {
		if ( null === self::$instance ) {
			self::$instance = new self();
		}

		return self::$instance;
	}

	/**
	 * Creates every feature and lets it add its hooks. Runs on plugins_loaded.
	 */
	public function boot(): void {
		/**
		 * Filters the feature classes the plugin starts.
		 *
		 * @since 1.0.0
		 *
		 * @param string[] $classes Fully qualified class names of Feature implementations.
		 */
		$classes = apply_filters( 'pagesco_books_features', $this->feature_classes() );

		foreach ( $classes as $class ) {
			$feature = new $class();
			$feature->register();
			$this->features[ $class ] = $feature;
		}
	}

	/**
	 * Returns a running feature, for example to remove one of its hooks.
	 *
	 * @param string $class_name Fully qualified class name.
	 */
	public function feature( string $class_name ): ?Feature {
		return $this->features[ $class_name ] ?? null;
	}

	/**
	 * The plugin's features. Add a new feature class here.
	 *
	 * @return string[]
	 */
	private function feature_classes(): array {
		return array(
			StoreNotice::class,
			BookPostType::class,
			GenreTaxonomy::class,
			BookMeta::class,
			Admin\BookMetaBox::class,
			Admin\BookColumns::class,
			Admin\StockAction::class,
			Settings::class,
			Admin\SettingsPage::class,
			EventsTable::class,
			Shortcodes\BookShortcode::class,
			Shortcodes\EventsShortcode::class,
			Blocks::class,
			BookBindings::class,
			Admin\StockWidget::class,
			Rest\BooksEndpoint::class,
			Rest\EventsEndpoint::class,
			Supplier\Availability::class,
			DailySync::class,
			Abilities::class,
			Holds\HoldsTable::class,
			Holds\HoldMail::class,
			Holds\HoldActions::class,
			Admin\HoldsPage::class,
			Rest\HoldsEndpoint::class,
		);
	}
}
